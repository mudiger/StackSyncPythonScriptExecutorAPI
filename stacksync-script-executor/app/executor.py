#Saarthak Mudigere Girsh
#saarthakmudigere@gmail.com
#6823923698

import subprocess
import tempfile
import json
import re

def run_script(script):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp:
            #write to temp file
            temp.write(script)
            temp.write("\n\nif __name__ == '__main__':\n")
            temp.write("    import json\n")
            temp.write("    try:\n")
            temp.write("        result = main()\n")
            temp.write("        print('__RESULT_START__' + json.dumps(result) + '__RESULT_END__')\n")
            temp.write("    except Exception as e:\n")
            temp.write("        print('__RESULT_START__' + json.dumps({'error': str(e)}) + '__RESULT_END__')\n")
            temp.flush()

            #print temp file
            print(f"Temp file path: {temp.name}")
            with open(temp.name, 'r') as f:
                contents = f.read()
                print("===== File Contents =====")
                print(contents)
                print("=========================")
            
            #run python script in nsjail isolation
            cmd = [
                "/usr/local/bin/nsjail",
                "--config", "nsjail.cfg",
                "--",
                "/usr/bin/env", 
                "LD_LIBRARY_PATH=/usr/local/lib",
                "/usr/local/bin/python3", temp.name
            ]

            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)

            #error if python script throws an error
            if proc.returncode != 0:
                return None, None, proc.stderr

            stdout = proc.stdout

            #extract return value from special markers
            match = re.search(r"__RESULT_START__(.*?)__RESULT_END__", stdout, re.DOTALL)
            if not match:
                return None, stdout, "Missing return value from main()"

            result_json = match.group(1)
            result = json.loads(result_json)

            #remove result line from stdout
            clean_stdout = re.sub(r"__RESULT_START__.*?__RESULT_END__", "", stdout, flags=re.DOTALL).strip()
            stdout_lines = clean_stdout.splitlines()

            return result, stdout_lines, None

    #catch error
    except Exception as e:
        return None, None, str(e)