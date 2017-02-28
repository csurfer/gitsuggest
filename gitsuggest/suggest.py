# -*- coding: utf-8 -*-

"""
git_suggest.suggest
~~~~~~~~~~~~~~~~~~~

This module contains the primary objects that power GitSuggest.
"""

import itertools

import enchant
import github
import nltk
from gensim import corpora, models
from nltk.tokenize import RegexpTokenizer


class GitSuggest(object):
    """Class to suggest git repositories for a user."""

    def __init__(self, username, password):
        """Constructor.

        :param username: Github username.
        :param password: Github password.
        """
        try:
            authenticated_user = github.Github(username, password)

            # Checking for authentication by fetching a property which on an
            # un-authenticated account would throw an exception.
            authenticated_user.get_user().name

            self.github = authenticated_user
        except github.GithubException:
            raise ValueError('Unable to authenticate the user.')

    def get_repos_for_query(self, query, count=10):
        """Method to procure git repositories for the query provided.

        :param query: String representing the repositories intend to search.
        :param count: Number of repositories to yeild.
        :return: Yields min(`count`, fetched) number of repositories for the
        query.
        """
        repo_gen = self.github.search_repositories(query, 'stars', 'desc')
        for index, repo in enumerate(repo_gen):
            if index < count:
                yield repo
            else:
                break

    def get_suggested_repositories(self):
        """Method to procure suggested repositories for the user.

        :return: Suggested repositories for the authenticated user.
        """
        # Procure query for repository suggestion.
        query = self.__get_query_for_repos()

        # Suggest repositories to the user.
        return self.get_repos_for_query(query)

    def __get_interests(self):
        """Method to procure description of repositories the user is already
        interested in.

        :return: List of repository descriptions.
        """
        repo_desc = set()

        # Add starred repositories of the authenticated user.
        cur_user = self.github.get_user()
        repo_desc.update([repo.description for repo in cur_user.get_starred()])

        """
        # Add starred repositories of users followed by authenticated user.
        # NOTE: Too time consuming at the moment.
        """
        for user in cur_user.get_following():
            repo_desc.update([repo.description for repo in user.get_starred()])

        return list(repo_desc)

    def __get_words_to_ignore(self):
        """Compiles list of all words to ignore.

        :return: List of words to ignore.
        """
        english_stopwords = nltk.corpus.stopwords.words('english')
        git_languages = []
        with open('../gitlang/languages.txt', 'r') as langauges:
            git_languages = [line.strip() for line in langauges]

        return list(itertools.chain(english_stopwords, git_languages))

    def __get_words_to_consider(self):
        """Compiles list of all words to consider.

        :return: List of words to consider.
        """
        return enchant.Dict("en_US")

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

        # Clean doc_lists.
        doc_list = [doc for doc in doc_list if doc is not None]

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

    def __get_query_for_repos(self, term_count=5):
        """Method to procure query based on topics authenticated user is
        interested in.

        :return: Query string.
        """
        # Get interests of authenticated user.
        docs = self.__get_interests()

        # Clean and tokenize the description strings.
        docs = self.__clean_and_tokenize(docs)

        # Setup LDA requisites.
        dictionary = corpora.Dictionary(docs)
        corpus = [dictionary.doc2bow(text) for text in docs]

        # Generate LDA model
        ldamodel = models.ldamodel.LdaModel(
            corpus, num_topics=1, id2word=dictionary, passes=10)

        repo_query_terms = []
        for term in ldamodel.get_topic_terms(0, topn=term_count):
            repo_query_terms.append(ldamodel.id2word[term[0]])

        return ' '.join(repo_query_terms)
