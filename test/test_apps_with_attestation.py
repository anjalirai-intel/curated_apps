import os
import pytest
import libs.curated_app_libs

yaml_file_name = "tests_with_attestation.yaml"
tests_yaml_path = os.path.join(os.getcwd(), 'data', yaml_file_name)

@pytest.mark.usefixtures("copy_repo")
@pytest.mark.usefixtures("curated_setup")
class TestClass:

    def test_redis_with_attestation(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_attestation(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_cert_file(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_cert_file_runtime_variables(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_end_test_ssl_path(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_sign_key(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_local_docker_image_with_attestation(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_end_test_ssl_path(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_local_docker_image_with_attestation(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_test_option(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_invalid_cert_option(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_and_empty_ssl(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_ssl_ca_crt(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_wo_ssl(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_default_cert(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_attestation_invalid_encrypted_option(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_attestation_no_encrypted_files(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_attestation_invalid_encrypted_files(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_attestation_encrypted_file_fullpath(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_pytorch_with_attestation_encrypted_file_invalid_format(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_client_conn(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

    def test_redis_with_attestation_verifier_kill(self):
        test_result = libs.curated_app_libs.run_test(self, tests_yaml_path)
        assert test_result

