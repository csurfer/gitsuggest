# -*- coding: utf-8 -*-

"""
gitsuggest.suggest
~~~~~~~~~~~~~~~~~~

This module contains the primary objects that power GitSuggest.
"""

import itertools
from operator import attrgetter

import enchant
import github
import nltk
from gensim import corpora, models
from nltk.tokenize import RegexpTokenizer


class GitSuggest(object):
    """Class to suggest git repositories for a user."""

    # Length of description of a repository over which it is a high chance
    # that it is a spammy repository.
    MAX_DESC_LEN = 300

    def __init__(self, username, password):
        """Constructor.

        :param username: Github username.
        :param password: Github password.
        """
        # Authenticated github user.
        self.github = None
        # Repositories authenticated user is interested in.
        self.__repositories_interested_in = None
        # Cleaned and sanitized tokens.
        self.__cleaned_tokens = None
        # Constructed LDA model.
        self.lda_model = None
        # Suggested repository set.
        self.suggested_repositories = None

        try:
            authenticated_user = github.Github(username, password)

            # Checking for authentication by fetching a property which on an
            # un-authenticated account would throw an exception.
            authenticated_user.get_user().name

            self.github = authenticated_user
        except github.GithubException:
            raise ValueError('Unable to authenticate the user.')

    def get_suggested_repositories(self):
        """Method to procure suggested repositories for the user.

        :return: Iterator to procure suggested repositories for the user.
        """
        if self.suggested_repositories is None:
            # Procure repositories to suggest to user.
            repository_set = set()
            for term_count in range(5, 2, -1):
                query = self.__get_query_for_repos(term_count=term_count)
                repository_set.update(self.__get_repos_for_query(query))

            # Remove repositories authenticated user is already interested in.
            already_starred = self.__repositories_interested_in
            catchy_repos = list(repository_set - already_starred)

            # Filter out repositories with too long descriptions. This is a
            # measure to weed out spammy repositories.
            filtered_repos = []

            if len(catchy_repos) > 0:
                for repo in catchy_repos:
                    if repo is not None and \
                       repo.description is not None and \
                       len(repo.description) <= GitSuggest.MAX_DESC_LEN:
                        filtered_repos.append(repo)

            # Present the repositories, highly starred to not starred.
            filtered_repos = sorted(filtered_repos,
                                    key=attrgetter('stargazers_count'),
                                    reverse=True)

            self.suggested_repositories = list()

            # TODO: Investigate why set(repositories) still not able to remove
            # duplicates.
            for repo in filtered_repos:
                if len(self.suggested_repositories) == 0:
                    self.suggested_repositories.append(repo)
                elif self.suggested_repositories[-1].description != \
                        repo.description:
                    self.suggested_repositories.append(repo)

        # Return an iterator to help user fetch the repository listing.
        for repository in self.suggested_repositories:
            yield repository

    def __get_interests(self):
        """Method to procure description of repositories the authenticated user
        is interested in.

        We currently attribute interest to:
        1. The repositories the authenticated user has starred.
        2. The repositories the users the authenticated user follows have
        starred.

        :return: List of repository descriptions.
        """
        if self.__repositories_interested_in is None:
            self.__repositories_interested_in = set()

            # Add starred repositories of the authenticated user.
            cur_user = self.github.get_user()
            self.__repositories_interested_in.update(cur_user.get_starred())

            # Add starred repositories of users followed by authenticated user.
            # NOTE: Too time consuming at the moment.
            for user in cur_user.get_following():
                self.__repositories_interested_in.update(user.get_starred())

        # Extract descriptions out of repositories of interest.
        repo_desc = [r.description for r in self.__repositories_interested_in]
        return list(set(repo_desc))

    def __get_words_to_ignore(self):
        """Compiles list of all words to ignore.

        :return: List of words to ignore.
        """
        # Stop words in English.
        english_stopwords = nltk.corpus.stopwords.words('english')

        # Languages in git repositories.
        git_languages = []
        with open('../gitlang/languages.txt', 'r') as langauges:
            git_languages = [line.strip() for line in langauges]

        # Other words to avoid in git repositories.
        words_to_avoid = []
        with open('../gitlang/others.txt', 'r') as languages:
            words_to_avoid = [line.strip() for line in languages]

        return list(itertools.chain(english_stopwords, git_languages,
                                    words_to_avoid))

    def __get_words_to_consider(self):
        """Compiles list of all words to consider.

        :return: List of words to consider.
        """
        return enchant.Dict('en_US')

    def __clean_and_tokenize(self, doc_list):
        """Method to clean and tokenize the document list.

        :param doc_list: Document list to clean and tokenize.
        :return: Cleaned and tokenized document list.
        """
        cleaned_doc_list = list()

        # Regular expression to remove out all punctuations, numbers and other
        # un-necessary text substrings like emojis etc.
        tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

        # Get stop words.
        stopwords = self.__get_words_to_ignore()

        # Get english words.
        dict_words = self.__get_words_to_consider()

        for doc in doc_list:
            # Lowercase doc.
            lower = doc.lower()

            # Tokenize removing numbers and punctuation.
            tokens = tokenizer.tokenize(lower)

            # Include meaningful words.
            tokens = [tok for tok in tokens if dict_words.check(tok)]

            # Remove stopwords.
            tokens = [tok for tok in tokens if tok not in stopwords]

            cleaned_doc_list.append(tokens)

        return cleaned_doc_list

    def __construct_lda_model(self):
        """Method to create LDA model to procure list of topics from.

        We do that by first fetching the descriptions of repositories user has
        shown interest in. We tokenize the hence fetched descriptions to
        procure list of cleaned tokens by dropping all the stop words and
        langauge names from it.

        We use the cleaned and sanitized token list to train LDA model from
        which we hope to procure topics of interests to the authenticated user.
        """
        # Fetch descriptions of repos of interest to authenticated user.
        repos_of_interest = self.__get_interests()

        # Some repositories fill entire documentation in description. We ignore
        # such repositories for cleaner tokens.
        repos_of_interest = filter(
            lambda x: x is not None and len(x) <= GitSuggest.MAX_DESC_LEN,
            repos_of_interest)

        # Procure clean tokens from the descriptions.
        cleaned_tokens = self.__clean_and_tokenize(repos_of_interest)

        # Setup LDA requisites.
        dictionary = corpora.Dictionary(cleaned_tokens)
        corpus = [dictionary.doc2bow(text) for text in cleaned_tokens]

        # Generate LDA model
        self.lda_model = models.ldamodel.LdaModel(
            corpus, num_topics=1, id2word=dictionary, passes=10)

    def __get_query_for_repos(self, term_count=5):
        """Method to procure query based on topics authenticated user is
        interested in.

        :return: Query string.
        """
        if self.lda_model is None:
            self.__construct_lda_model()

        repo_query_terms = []
        for term in self.lda_model.get_topic_terms(0, topn=term_count):
            repo_query_terms.append(self.lda_model.id2word[term[0]])

        return ' '.join(repo_query_terms)

    def __get_repos_for_query(self, query):
        """Method to procure git repositories for the query provided.

        :param query: String representing the repositories intend to search.
        :return: Iterator for repositories found using the query.
        """
        return self.github.search_repositories(query, 'stars', 'desc')
