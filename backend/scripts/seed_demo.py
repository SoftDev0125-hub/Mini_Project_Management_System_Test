from core.models import Organization, Project, Task, TaskComment

orgs = [
    ("alpha", "Alpha Org", "alpha@example.com"),
    ("beta", "Beta Org", "beta@example.com"),
    ("gamma", "Gamma Org", "gamma@example.com"),
]

for slug, name, email in orgs:
    org, _ = Organization.objects.get_or_create(slug=slug, defaults={"name": name, "contact_email": email})
    for i in range(1, 3):
        project, _ = Project.objects.get_or_create(organization=org, name=f"{name} Project {i}", defaults={"description": "Demo project"})
        for j in range(1, 6):
            task, _ = Task.objects.get_or_create(
                project=project,
                title=f"Task {j} for {project.name}",
                defaults={"description": "Demo task", "assignee_email": f"user{j}@example.com", "status": "TODO"},
            )
            TaskComment.objects.get_or_create(task=task, content="Initial comment", author_email="seed@example.com")

print("Demo seed complete")
