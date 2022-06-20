# Development Environment Setup

## Hyperledger Sawtooth testing environment

Several issues occurred while setting up the docker testing environment (which appeared to be optimal) outlined in the documentation ([Setting up a Sawtooth Node for Testing](https://sawtooth.hyperledger.org/docs/1.2/app_developers_guide/installing_sawtooth.html) or [Creating a Sawtooth Test Network](https://sawtooth.hyperledger.org/docs/1.2/app_developers_guide/creating_sawtooth_network.html)), which caused the setups to fail. Suppose it is the case that Hyperledger sawtooth is not behaving as intended during the procedure outlined in the documentation. In that case, this section provides a potential solution that is guaranteed to work as it relies on google virtual machines (the specification for which is outlined below). It is also a representative of how the testing/development environment was set up when during development.

### Requirements
Since google cloud was used, this setup requires a working credit or debit card. The costs of using a google cloud vm can be found here: [VM instance pricing](https://cloud.google.com/compute/vm-instance-pricing). To find out the exact pricing of the used VM instance (see the **Relevant Machine Specification** section).

### Relevant Machine Specification

**Note**: In case some part of the specification is not outlined, it can then be assumed that the default value was used.

Machine type: n2-standard-2

CPU platform: Intel Ice Lake

Image: ubuntu-2204-jammy-v20220607 *Docker may not be supported by your operating system of choice (see [Install Docker Engine](https://docs.docker.com/engine/install/))*

Size: 100GB *The system had a single drive*

**Google cloud shell command used for VM instantiation**:
```
gcloud compute instances create <system_name> \
    --project=<project_id> \
    --zone=europe-west4-a \
    --machine-type=n2-standard-2 \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE --provisioning-model=STANDARD \
    --min-cpu-platform=Intel\ Ice\ Lake \
    --create-disk=auto-delete=yes,boot=yes,device-name=<device_name> image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20220607,mode=rw,size=100,type=projects/hyperledgerdev-352612/zones/europe-west4-a/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any \
    --enable-nested-virtualization
```

Executing this command will result in the same VM instance used during project development. Symbols `<>` should be replaced with own values.

**Note**: It is vital to instantiate the machine with the ``--enable-nested-virtualization`` option, as it ensures that the VM is able to run docker containers. Nested virtualization is not supported by every google VM instance, for more information see [About nested virtualization](https://cloud.google.com/compute/docs/instances/nested-virtualization/overview) and [Enabling nested virtualization](https://cloud.google.com/compute/docs/instances/nested-virtualization/enabling).

### Docker installation

Install Docker Engine [Install Docker Engine](https://docs.docker.com/engine/install/) and Docker compose [Install Docker Compose](https://docs.docker.com/compose/install/).

#### GUI installation
You might consider it useful to be able to access your VM through a GUI for this see guides [Launch Ubuntu Desktop on Google Cloud](https://ubuntu.com/blog/launch-ubuntu-desktop-on-google-cloud) and [Install Chrome Remote Desktop...](https://bytexd.com/install-chrome-remote-desktop-headless/)

#### KVM configuration

Before launching Docker, install KVM: [KVM Installation](https://help.ubuntu.com/community/KVM/Installation)


# Helpful resources

TODO: Format https://www.youtube.com/watch?v=4VUaZkwJdCc