import graphene
from graphene_django import DjangoObjectType
from .models import Organization, Project, Task, TaskComment
from django.db.models import Count, Q


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'slug', 'contact_email')


class ProjectType(DjangoObjectType):
    task_count = graphene.Int()
    completed_tasks = graphene.Int()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'status', 'due_date', 'organization')

    def resolve_task_count(self, info):
        return self.tasks.count()

    def resolve_completed_tasks(self, info):
        return self.tasks.filter(status='DONE').count()


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'assignee_email', 'due_date', 'project')


class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = ('id', 'task', 'content', 'author_email', 'timestamp')


class Query(graphene.ObjectType):
    projects_by_org = graphene.List(ProjectType, org_slug=graphene.String(required=True))
    project_stats = graphene.Field(lambda: graphene.JSONString, org_slug=graphene.String(required=True))

    def resolve_projects_by_org(self, info, org_slug):
        try:
            org = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            return []
        return Project.objects.filter(organization=org).prefetch_related('tasks')

    def resolve_project_stats(self, info, org_slug):
        try:
            org = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            return {}
        projects = Project.objects.filter(organization=org).annotate(total_tasks=Count('tasks'), completed=Count('tasks', filter=Q(tasks__status='DONE')))
        return {p.id: {'name': p.name, 'total': p.total_tasks, 'completed': p.completed} for p in projects}


class CreateProject(graphene.Mutation):
    class Arguments:
        org_slug = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        due_date = graphene.types.datetime.Date()

    project = graphene.Field(ProjectType)

    def mutate(self, info, org_slug, name, description=None, due_date=None):
        org = Organization.objects.get(slug=org_slug)
        project = Project.objects.create(organization=org, name=name, description=description or '', due_date=due_date)
        return CreateProject(project=project)


class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()

    task = graphene.Field(TaskType)

    def mutate(self, info, project_id, title, description=None):
        project = Project.objects.get(id=project_id)
        task = Task.objects.create(project=project, title=title, description=description or '')
        return CreateTask(task=task)


class AddComment(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        content = graphene.String(required=True)
        author_email = graphene.String(required=True)

    comment = graphene.Field(TaskCommentType)

    def mutate(self, info, task_id, content, author_email):
        task = Task.objects.get(id=task_id)
        comment = TaskComment.objects.create(task=task, content=content, author_email=author_email)
        return AddComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    create_task = CreateTask.Field()
    add_comment = AddComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
