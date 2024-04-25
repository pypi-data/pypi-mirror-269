import subprocess
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from r_shepard.api.models import Project


@shared_task
def auto_commit():
    # Only do this for projects where auto_commit is enabled
    projects = Project.objects.filter(auto_commit_enabled=True)

    for project in projects:
        # Check if it's time to commit
        try:
            now = timezone.now()
            if now - project.last_commit_time >= timedelta(
                minutes=project.commit_interval
            ):
                # Commit and push changes
                subprocess.run(["git", "add", "."], cwd=project.workspace_path)
                subprocess.run(
                    ["git", "commit", "-m", "Auto-commit"], cwd=project.workspace_path
                )
                subprocess.run(
                    ["git", "push", project.git_repo_url], cwd=project.workspace_path
                )
                # Update the last commit time
                project.last_commit_time = now
                project.save()
            else:
                print(f"Not time to commit for project {project.slug}")
        except subprocess.CalledProcessError as e:
            print(f"Encountered git error for project {project.slug}: {e}")
        except Exception as e:
            print(f"Failed to auto-commit for project {project.slug}: {e}")
