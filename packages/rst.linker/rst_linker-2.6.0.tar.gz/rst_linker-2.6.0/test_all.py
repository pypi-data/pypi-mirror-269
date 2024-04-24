import locale
import textwrap

import pytest
from path import Path

import rst.linker


@pytest.fixture(scope='session', autouse=True)
def stable_locale():
    """
    Fix locale to avoid failed tests under other locales.
    """
    locale.setlocale(locale.LC_ALL, 'C')


@pytest.fixture
def linker_defn():
    return dict(
        using=dict(kiln='https://org.kilnhg.com/Code/Repositories'),
        replace=[
            dict(
                pattern=r"proj (?P<proj_ver>\d+(\.\d+)*([abc]\d+)?)",
                url='{kiln}/repo/proj/Files/CHANGES?rev={proj_ver}',
            ),
            dict(
                pattern=r"(Case |#)(?P<id>\d+)",
                url='https://org.fogbugz.com/f/cases/{id}/',
            ),
        ],
    )


def test_linker_example(linker_defn):
    repl = rst.linker.Replacer.from_definition(linker_defn)
    assert 'kilnhg' in repl.run(
        """
        proj 1.0 was released
        """
    )


def test_write_links(linker_defn):
    repl = rst.linker.Replacer.from_definition(linker_defn)
    source = Path('foo.txt')
    dest = Path('foo.out')
    source.write_text(
        """
        1.0
        ---

        proj 1.0 was released
        """,
        encoding='utf-8',
    )
    repl.write_links(source, dest)
    res = dest.read_text(encoding='utf-8')
    assert 'kilnhg' in res
    source.remove()
    dest.remove()


@pytest.fixture
def scm_defn():
    return dict(
        replace=[
            dict(
                pattern=r"(?m:^((?P<scm_version>\d+(\.\d+){1,2}))\n-+\n)",
                with_scm="{text}\nTagged {rev[timestamp]}\n",
            )
        ]
    )


@pytest.fixture()
def fake_git(fp):
    fp.register(['git', 'status'])
    fp.register(['git', 'version'], stdout='git version 2.44.0')
    fp.register(['git', 'log', fp.any(), '1.0'], stdout='2015-02-24 22:41:28 -0600')
    fp.register(['git', 'log', fp.any(), '1.3'], stdout='2016-02-12 11:05:47 -0500')


def test_scm_example(scm_defn, fake_git):
    repl = rst.linker.Replacer.from_definition(scm_defn)
    input = textwrap.dedent(
        """
        1.0
        ---

        Some details
        """
    )
    result = repl.run(input)
    assert 'Tagged 2015-02' in result


def test_scm_custom_date_format(scm_defn, fake_git):
    with_scm = textwrap.dedent(
        """
        {text}
        Copyright {rev[timestamp]:%Y}
        Released {rev[timestamp]:%d-%b}
        """
    )
    scm_defn['replace'][0]['with_scm'] = with_scm
    repl = rst.linker.Replacer.from_definition(scm_defn)
    changelog = textwrap.dedent(
        """
        1.0
        ---

        Some details
        """
    )
    result = repl.run(changelog)
    assert "Copyright 2015" in result
    assert "Released 24-Feb" in result


def test_combined(scm_defn, linker_defn, fake_git):
    defn = linker_defn
    defn['replace'].extend(scm_defn['replace'])
    repl = rst.linker.Replacer.from_definition(defn)
    input = textwrap.dedent(
        """
        1.3
        ---

        Bumped to proj 1.1.
        """
    )
    result = repl.run(input)
    assert 'Tagged 2016-02' in result
    assert 'https://org.kilnhg' in result


def test_deselected(scm_defn):
    """
    A URLLinker should resolve to False when initialized with an
    scm definition.
    """
    repl = rst.linker.URLLinker(scm_defn)
    assert not repl
