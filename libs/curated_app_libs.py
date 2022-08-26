import inspect
import subprocess
import sys
import os
from data.constants import *
from libs import config_parser
from libs import utils
from libs import workload
import time
import re


def get_curation_cmd(test_config_dict):
    workload_image = test_config_dict["docker_image"]
    debug_mode = ''
    if test_config_dict.get("debug_mode") == 'y':
        debug_mode = '-d '
    if test_config_dict.get("test_option"):
        curation_cmd = 'sudo python3 curate.py ' + debug_mode + workload_image + ' test < input.txt'
    else:
        curation_cmd = 'sudo python3 curate.py ' + debug_mode + workload_image + ' < input.txt'
    return curation_cmd

def write_to_log_file(tc_dict, output):
    fd = open(os.path.join(FRAMEWORK_PATH, tc_dict['log_file']), "w")
    fd.write(output)
    fd.close()

def screen_verification(output):
    if "This application will provide step-by-step guidance" in output:
        return "home_page"
    elif "Please provide path to your signing key in the blue box" in output:
        return "signing_page"
    elif "To enable remote attestation using Azure DCAP client" in output:
        return "attestation_page"
    elif "Building the RA-TLS Verifier image" in output:
        return "verifier_page"
    elif "Specify docker run-time arguments here" in output:
        return "runtime_page"
    elif "Please specify a list of env variables" in output:
        return "environment_page"
    elif "If the base image contain encrypted data, please provide" in output:
        return "encrypted_page"
    elif "The curated GSC image gsc-redis:latest is ready" in output:
        return "final_page"

def test_should_break(screen_name, expected_screen):
    pos = SCREEN_LIST.index(screen_name)
    if expected_screen not in SCREEN_LIST[pos:]:
        return True

def generate_curated_image(test_config_dict):
    curation_output = ''

    curation_cmd = get_curation_cmd(test_config_dict)
    end_test = test_config_dict.get('expected_output_console')
    os.chdir(CURATED_APPS_PATH)
    try:
        process = subprocess.Popen(curation_cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
        print("Process started ", curation_cmd)
        os.chdir(FRAMEWORK_PATH)
        screen_name = "home_page"
        while True:
            output = process.stdout.readline()
            if process.poll() is not None and output == '':
                break
            if output:
                curation_output += output
                value = screen_verification(output)
                if value: screen_name = value
                if 'expected_output_console' in test_config_dict.keys():
                    should_break = test_should_break(screen_name, test_config_dict['expected_screen'])
                    if end_test in output or should_break:
                        break
    finally:
        process.stdout.close()
        utils.kill(process.pid)
    write_to_log_file(test_config_dict, curation_output)
    return curation_output

def get_docker_run_command(attestation, workload_name):
    output = []
    wrapper_image = "gsc-{}".format(workload_name)
    ssl_path = os.path.join(VERIFIER_SERVICE_PATH,"ssl_common")
    if attestation == 'test' or attestation == 'done':
        verifier_cmd  = "docker run --rm --net=host -e RA_TLS_ALLOW_DEBUG_ENCLAVE_INSECURE=1 -e RA_TLS_ALLOW_OUTDATED_TCB_INSECURE=1 -v {}:/ra-tls-secret-prov/ssl --device=/dev/sgx/enclave  -t verifier_image:latest".format(ssl_path)
        gsc_workload = "docker run --rm --net=host --device=/dev/sgx/enclave -e SECRET_PROVISION_SERVERS=\"localhost:4433\" \
            -v /var/run/aesmd/aesm.socket:/var/run/aesmd/aesm.socket -t {}".format(wrapper_image)
        output.append(verifier_cmd)
    else:
        gsc_workload = "docker run --rm --net=host --device=/dev/sgx/enclave -t {}".format(wrapper_image)
    output.append(gsc_workload)
    return output

def get_workload_result(workload_name):
    pytorch_result = ["Result", "Labrador retriever", "golden retriever", "Saluki, gazelle hound", "whippet", "Ibizan hound, Ibizan Podenco"]
    bash_result = ["total        used        free      shared  buff/cache   available"]
    redis_result = ["Ready to accept connections"]
    if "bash" in workload_name:
        workload_result = bash_result
    elif "redis" in workload_name:
        workload_result = redis_result
    elif "pytorch" in workload_name:
        workload_result = pytorch_result
    return workload_result

def verify_debug_log(log):
    result = False
    debug_log_statements = ["debug: Adding pages to SGX enclave, this may take some time...", 
                           "debug: Added all pages to SGX enclave", 
                           "debug: Gramine parsed TOML manifest file successfully", 
                           "debug: Key exchange succeeded"]
    if  all(x in log for x in debug_log_statements):
        result = True
        print("Debug logs are available")
    return result

def expected_msg_verification(test_config_dict, curation_output):
    result = False
    if "expected_output_infile" in test_config_dict.keys():
        base_image_name = test_config_dict.get("docker_image").split('/', maxsplit=1)[1]
        base_image_type = test_config_dict.get("docker_image").split('/', maxsplit=1)[0]
        log_file_name, n = re.subn('[:/]', '_', base_image_name)
        log_file = f'{base_image_type}/{log_file_name}.log'
        with open(os.path.join(CURATED_APPS_PATH, log_file), "r") as log_file_pointer:
            for line in log_file_pointer.readlines():
                print(line)
                if test_config_dict.get("expected_output_infile") in line:
                    result = True
            return result

    if "expected_output_console" in test_config_dict.keys():
        if test_config_dict.get("expected_output_console") in curation_output:
            result = True
        return result
    return None

def run_curated_image(docker_command, workload_name, attestation=None, debug_mode=''):
    result = False
    run_log = []
    workload_result = get_workload_result(workload_name)
    gsc_docker_command = docker_command[-1]
    if attestation == 'test' or attestation == 'done':
        verifier_process = utils.popen_subprocess(docker_command[0])
        time.sleep(20)

    process = utils.popen_subprocess(gsc_docker_command)
    while True:
        nextline = process.stdout.readline()
        run_log.append(nextline.strip())
        print(nextline.strip())
        if nextline == '' and process.poll() is not None:
            break
        if  all(x in nextline for x in workload_result):
            process.stdout.close()
            if attestation == 'test' or attestation == 'done':
                utils.kill(verifier_process.pid)
            utils.kill(process.pid)
            sys.stdout.flush()
            if debug_mode:
                if not verify_debug_log(run_log):
                    break
            result = True
            break
    return result

def verify_run(curation_output):
    if re.search("The curated GSC image gsc-(.*) is ready", curation_output) or \
            re.search("docker run", curation_output):
        return True
    return False

def run_test(test_instance, test_yaml_file):
    result = False
    test_name = inspect.stack()[1].function
    print(f"\n********** Executing {test_name} **********\n")
    test_config_dict = config_parser.read_config_yaml(test_yaml_file, test_name)
    utils.test_setup(test_config_dict)
    debug_mode = utils.is_debug_mode(test_config_dict)
    try:
        workload_name = utils.get_workload_name(test_config_dict['docker_image'])
        curation_output = generate_curated_image(test_config_dict)
        result = expected_msg_verification(test_config_dict, curation_output)
        if result == None:
            if verify_run(curation_output):
                docker_run = get_docker_run_command(test_config_dict['attestation'], workload_name)
                result = run_curated_image(docker_run, workload_name, test_config_dict['attestation'], debug_mode)
                if result and "redis" in test_name:
                    result = workload.run_redis_client()
    finally:
        print("Docker images cleanup")
        utils.cleanup_after_test(workload_name)
    return result

