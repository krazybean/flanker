# coding:utf-8
"""
Spelling corrector library, used to correct common typos in domains like
gmal.com instead of gmail.com.

The spelling corrector uses difflib which in turn uses the
Ratcliff-Obershelp algorithm [1] to compute the similarity of two strings.
This is a very fast an accurate algorithm for domain spelling correction.

The (only) public method this module has is suggest(word), which given
a domain, suggests an alternative or returns the original domain
if no suggestion exists.

[1] http://xlinux.nist.gov/dads/HTML/ratcliffObershelp.html
"""

import re
import time
import difflib
from collections import Counter
from Levenshtein import ratio


def suggest(word, cutoff=0.77, override=None, algo='difflib'):
    """
    Given a domain and a cutoff heuristic, suggest an alternative or return the
    original domain if no suggestion exists.
    """
    word_list = override if override else MOST_COMMON_DOMAINS

    if word in LOOKUP_TABLE:
        return LOOKUP_TABLE[word]

    if algo == 'levenshtein':
        guess = levenshtein(word, word_list, cutoff=cutoff)
    elif algo == 'spellr':
        guess = spelling(word, word_list)
    else:
        guess = difflib.get_close_matches(word, word_list, n=1, cutoff=cutoff)

    if guess and len(guess) > 0:
        return guess[0]
    return word


def levenshtein(word, word_list, n=1, cutoff=0.80):
    """
    Attempted implementation of Levenshtein c extension
    """
    matches = list()
    matches.append([domain for domain in word_list if ratio(word, domain) > cutoff and len(matches) <= n])
    return matches[0]


def spelling(word, word_list, n=1, cutoff=0.00):
    """
    Implemented norvig's solution from: http://norvig.com/spell-correct.html
    For additional variety of potential solutions.

    Otherwise i'm not a fan of nested functions
    """
    WORDS = Counter(word_list)

    def probability(word, WORDS):
        N = sum(WORDS.values())
        return WORDS[word] / N

    def correction(word):
        return max(candidates(word), key=probability)

    def candidates(word):
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

    def known(words):
        return set(w for w in words if w in words)

    def edits1(word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(word):
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    return correction(word)

MOST_COMMON_DOMAINS = [
    # mailgun :)
    'mailgun.net',
    # big esps
    '163.com',
    'aim.com',
    'alice.it',
    'aol.co.uk',
    'aol.com',
    'att.net',
    'azet.sk',
    'bell.net',
    'bellsouth.net',
    'bigpond.com',
    'bigpond.com.au',
    'bigpond.net.au',
    'bluewin.ch',
    'blueyonder.co.uk',
    'bol.com.br',
    'btinternet.com',
    'btopenworld.com',
    'cableone.net',
    'centrum.sk',
    'centurylink.net',
    'centurytel.net',
    'charter.net',
    'comcast.net',
    'cox.net',
    'cs.com',
    'earthlink.net',
    'email.com',
    'email.cz',
    'email.it',
    'embarqmail.com',
    'excite.com',
    'fastwebnet.it',
    'free.fr',
    'freemail.hu',
    'freenet.de',
    'frontier.com',
    'frontiernet.net',
    'fuse.net',
    'gmail.com',
    'gmx.at',
    'gmx.ch',
    'gmx.com',
    'gmx.de',
    'gmx.net',
    'google.com',
    'googlemail.com',
    'hanmail.net',
    'home.nl',
    'hotmail.be',
    'hotmail.ca',
    'hotmail.co.jp',
    'hotmail.co.nz',
    'hotmail.co.uk',
    'hotmail.com',
    'hotmail.com.ar',
    'hotmail.com.au',
    'hotmail.de',
    'hotmail.es',
    'hotmail.fr',
    'hotmail.gr',
    'hotmail.it',
    'hotmail.nl',
    'hotmail.no',
    'hotmail.se',
    'hughes.net',
    'icloud.com',
    'iinet.net.au',
    'inbox.lv',
    'inbox.ru',
    'interia.pl',
    'juno.com',
    'laposte.net',
    'libero.it',
    'list.ru',
    'live.be',
    'live.ca',
    'live.co.uk',
    'live.com',
    'live.com.ar',
    'live.com.au',
    'live.com.mx',
    'live.de',
    'live.dk',
    'live.fr',
    'live.it',
    'live.nl',
    'live.no',
    'live.se',
    'mac.com',
    'mail.com',
    'mail.ru',
    'me.com',
    'microsoft.com',
    'mindspring.com',
    'msn.com',
    'naver.com',
    'netscape.net',
    'netspace.net.au',
    'netzero.com',
    'netzero.net',
    'neuf.fr',
    'nhs.net',
    'ntlworld.com',
    'o2.pl',
    'online.no',
    'optimum.net',
    'optonline.net',
    'optusnet.com.au',
    'orange.fr',
    'ostrovok.ru',
    'outlook.com',
    'outlook.com.au',
    'outlook.de',
    'outlook.es',
    'outlook.fr',
    'outlook.it',
    'pacbell.net',
    'planet.nl',
    'prodigy.net',
    'prodigy.net.mx',
    'protonmail.com',
    'q.com',
    'qq.com',
    'rambler.ru',
    'reagan.com',
    'rediffmail.com',
    'roadrunner.com',
    'rocketmail.com',
    'rogers.com',
    'sbcglobal.net',
    'seznam.cz',
    'sfr.fr',
    'shaw.ca',
    'sky.com',
    'skynet.be',
    'suddenlink.net',
    'swbell.net',
    'sympatico.ca',
    't-online.de',
    'talktalk.net',
    'telefonica.net',
    'telenet.be',
    'telfort.nl',
    'telia.com',
    'telus.net',
    'telusplanet.net',
    'tiscali.co.uk',
    'tiscali.it',
    'ukr.net',
    'uol.com.br',
    'usa.net',
    'vepl.com',
    'verizon.net',
    'videotron.ca',
    'virgilio.it',
    'virgin.net',
    'virginmedia.com',
    'wanadoo.fr',
    'web.de',
    'windowslive.com',
    'windstream.net',
    'wp.pl',
    'xs4all.nl',
    'xtra.co.nz',
    'y7mail.com',
    'ya.ru',
    'yahoo.ca',
    'yahoo.co.id',
    'yahoo.co.in',
    'yahoo.co.jp',
    'yahoo.co.nz',
    'yahoo.co.uk',
    'yahoo.com',
    'yahoo.com.ar',
    'yahoo.com.au',
    'yahoo.com.br',
    'yahoo.com.hk',
    'yahoo.com.mx',
    'yahoo.com.my',
    'yahoo.com.ph',
    'yahoo.com.sg',
    'yahoo.com.tw',
    'yahoo.de',
    'yahoo.es',
    'yahoo.fr',
    'yahoo.gr',
    'yahoo.ie',
    'yahoo.in',
    'yahoo.it',
    'yahoo.no',
    'yahoo.se',
    'yandex.com',
    'yandex.ru',
    'ymail.com',
    'ziggo.nl',
    'zoominternet.net'
]

# domains that the corrector doesn't fix that we should fix
LOOKUP_TABLE = {
    u'yahoo':       u'yahoo.com',
    u'gmail':       u'gmail.com',
    u'hotmail':     u'hotmail.com',
    u'live':        u'live.com',
    u'outlook':     u'outlook.com',
    u'msn':         u'msn.com',
    u'googlemail':  u'googlemail.com',
    u'aol':         u'aol.com',
    u'aim':         u'aim.com',
    u'icloud':      u'icloud.com',
    u'me':          u'me.com',
    u'mac':         u'mac.com',
    u'facebook':    u'facebook.com',
    u'comcast':     u'comcast.net',
    u'sbcglobal':   u'sbcglobal.net',
    u'bellsouth':   u'bellsouth.net',
    u'verizon':     u'verizon.net',
    u'earthlink':   u'earthlink.net',
    u'cox':         u'cox.net',
    u'charter':     u'charter.net',
    u'shaw':        u'shaw.ca',
    u'bell':        u'bell.net'
}


if __name__ == '__main__':
    word = 'yahuo.com'

    def classic(word):
        start_time = time.time()
        output = suggest(word)
        duration = time.time() - start_time
        return float(duration), output

    def new(word):
        start_time = time.time()
        output = suggest(word, algo='levenshtein')
        duration = time.time() - start_time
        return float(duration), output

    def spellr(word):
        start_time = time.time()
        output = suggest(word, algo='levenshtein')
        duration = time.time() - start_time
        return float(duration), output

    difflib_time, difflib_out = classic(word)
    leve_time, leve_out = new(word)
    spell_time, spell_out = spellr(word)

    print("Algo difflib: {}".format(difflib_out))
    print("Difflib Time: %.20f or {}ms".format(difflib_time * 1000) % difflib_time)

    print("Algo leve: {}".format(leve_out))
    print("Leve Time: %.20f or {}ms".format(leve_time * 1000) % leve_time)

    print("Algo spell: {}".format(leve_out))
    print("Spell Time: %.20f or {}ms".format(spell_time * 1000) % spell_time)
