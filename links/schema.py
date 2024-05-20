import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from links.models import Answers, Vote
from graphql import GraphQLError



class LinkType(DjangoObjectType):
    class Meta:
        model = Answers

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        return Answers.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    answer = graphene.String()
    link = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        answer = graphene.String()
        link = graphene.String()

    #3
    def mutate(self, info, answer, link):
        user = info.context.user or None
        linkk = Answers(answer=answer, link=link, posted_by=user)
        linkk.save()

        return CreateLink(
            id=linkk.id,
            answer=linkk.answer,
            link=linkk.link,
            posted_by=linkk.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        link = Answers.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()