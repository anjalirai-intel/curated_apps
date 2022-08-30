import os

FRAMEWORK_PATH         = os.getcwd()
REPO_PATH              = os.path.join(FRAMEWORK_PATH, "contrib_repo")
ORIG_CURATED_PATH      = os.path.join(FRAMEWORK_PATH, "orig_contrib_repo")
CONTRIB_GIT_CMD        = "git clone https://github.com/aneessahib/contrib.git orig_contrib_repo"
GIT_CHECKOUT_CMD       = "git checkout aneessahib/gsc_curation"
CURATED_PATH           = "GSC-Image-Curation"
CURATED_APPS_PATH      = os.path.join(REPO_PATH, CURATED_PATH)
VERIFIER_SERVICE_PATH  = os.path.join(CURATED_APPS_PATH, "verifier")
VERIFIER_DOCKERFILE    = os.path.join(ORIG_CURATED_PATH, CURATED_PATH, "verifier/verifier.dockerfile.template")
PYTORCH_HELPER_PATH    = os.path.join(CURATED_APPS_PATH, "pytorch", "base_image_helper")
PYTORCH_HELPER_CMD     = f"bash {PYTORCH_HELPER_PATH}/helper.sh"
BASH_PATH              = os.path.join(CURATED_APPS_PATH, "bash")
BASH_TEST              = "bash-test"
SCREEN_LIST            = ["home_page", "signing_page", "attestation_page", "verifier_page", "runtime_page", "environment_page",
                          "encrypted_page", "encryption_key_page", "final_page"]
BASH_DOCKERFILE        = os.path.join(CURATED_APPS_PATH, "bash", "Dockerfile")
BASH_GSC_DOCKERFILE    = os.path.join(CURATED_APPS_PATH, "bash", "bash-gsc.dockerfile")
ENV_PROXY_STRING       = 'ENV http_proxy "http://proxy-dmz.intel.com:911"\nENV https_proxy "http://proxy-dmz.intel.com:912"\n'
AZURE_DCAP             = "(.*)RUN wget https:\/\/packages.microsoft(.*)\n(.*)amd64.deb"
GRAMINE_INSTALL        = "RUN apt-get install -y gramine-dcap"
DCAP_LIBRARY           = "\nRUN apt install -y libsgx-dcap-default-qpl libsgx-dcap-default-qpl-dev\nCOPY sgx_default_qcnl.conf  /etc/sgx_default_qcnl.conf"