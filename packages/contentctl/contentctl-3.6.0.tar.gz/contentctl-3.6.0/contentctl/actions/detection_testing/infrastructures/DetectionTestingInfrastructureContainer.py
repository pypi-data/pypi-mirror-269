from contentctl.actions.detection_testing.infrastructures.DetectionTestingInfrastructure import (
    DetectionTestingInfrastructure,
)
import docker.models.resource
import docker.models.containers
import docker
import docker.types
from contentctl.objects.test_config import (
    CONTAINER_APP_DIR,
    LOCAL_APP_DIR,
)


class DetectionTestingInfrastructureContainer(DetectionTestingInfrastructure):
    container: docker.models.resource.Model = None

    def start(self):
        if self.global_config.infrastructure_config.persist_and_reuse_container:
            # If we are configured to use the persistent container, then check and see if it's already
            # running. If so, just use it without additional configuration.
            try:
                self.container = self.get_docker_client().containers.get(self.get_name())
                return
            except Exception:
                #We did not find the container running, we will set it up
                pass

        self.container = self.make_container()
        self.container.start()

    def finish(self):
        if self.container is not None:
            try:
                self.removeContainer()
                pass
            except Exception as e:
                raise (Exception(f"Error removing container: {str(e)}"))
        super().finish()

    def get_name(self) -> str:
        return self.infrastructure.instance_name

    def get_docker_client(self):
        try:
            c = docker.client.from_env()

            return c
        except Exception as e:
            raise (Exception(f"Failed to get docker client: {str(e)}"))

    def check_for_teardown(self):

        try:
            self.get_docker_client().containers.get(self.get_name())
        except Exception as e:
            if self.sync_obj.terminate is not True:
                self.pbar.write(
                    f"Error: could not get container [{self.get_name()}]: {str(e)}"
                )
                self.sync_obj.terminate = True

        if self.sync_obj.terminate:
            self.finish()

        super().check_for_teardown()

    def make_container(self) -> docker.models.resource.Model:
        # First, make sure that the container has been removed if it already existed
        self.removeContainer()

        ports_dict = {
            "8000/tcp": self.infrastructure.web_ui_port,
            "8088/tcp": self.infrastructure.hec_port,
            "8089/tcp": self.infrastructure.api_port,
        }

        mounts = [
            docker.types.Mount(
                source=str(LOCAL_APP_DIR.absolute()),
                target=str(CONTAINER_APP_DIR.absolute()),
                type="bind",
                read_only=True,
            )
        ]

        environment = {}
        environment["SPLUNK_START_ARGS"] = "--accept-license"
        environment["SPLUNK_PASSWORD"] = self.infrastructure.splunk_app_password
        environment["SPLUNK_APPS_URL"] = ",".join(
            p.environment_path for p in self.global_config.apps 
        )
        if (
            self.global_config.splunkbase_password is not None
            and self.global_config.splunkbase_username is not None
        ):
            environment["SPLUNKBASE_USERNAME"] = self.global_config.splunkbase_username
            environment["SPLUNKBASE_PASSWORD"] = self.global_config.splunkbase_password

        container = self.get_docker_client().containers.create(
            self.global_config.infrastructure_config.full_image_path,
            ports=ports_dict,
            environment=environment,
            name=self.get_name(),
            mounts=mounts,
            detach=True,
            platform="linux/amd64"
        )

        return container

    def removeContainer(self, removeVolumes: bool = True, forceRemove: bool = True):
        try:
            container: docker.models.containers.Container = (
                self.get_docker_client().containers.get(self.get_name())
            )
        except Exception as e:
            # Container does not exist, no need to try and remove it
            return
        try:
            # If the user wants to persist the container (or use a previously configured container), then DO NOT remove it.
            # Emit the following message, which they will see on initial setup and teardown at the end of the test. 
            if self.global_config.infrastructure_config.persist_and_reuse_container:
                print(f"\nContainer [{self.get_name()}] has NOT been terminated because 'contentctl_test.yml ---> infrastructure_config ---> persist_and_reuse_container = True'")
                print(f"To remove it, please manually run the following at the command line: `docker container rm -fv {self.get_name()}`\n")
                return
            # container was found, so now we try to remove it
            # v also removes volumes linked to the container
            container.remove(v=removeVolumes, force=forceRemove)
            # remove it even if it is running. remove volumes as well
            # No need to print that the container has been removed, it is expected behavior

        except Exception as e:
            raise (
                Exception(
                    f"Could not remove Docker Container [{self.get_name()}]: {str(e)}"
                )
            )
