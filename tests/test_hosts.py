import sys
import pytest
from os import path
sys.path.append( path.dirname(path.dirname( path.abspath(__file__))))
from hosts.hosts import Hosts, HostsEntry


def test_add_single_ipv4_host_by_params(tmpdir):
    ''' add an ipv4 type entry '''
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost")
    print hosts_file.strpath
    hosts = Hosts(path=hosts_file.strpath)
    hosts.add(force=False, entry_type='ipv4', address='123.123.123.123', names=['test.example.com'])
    assert hosts.count(address="123.123.123.123").get('address_matches') == 1
    assert hosts.count(address="127.0.0.1").get('address_matches') == 1

def test_add_single_ipv4_host_with_by_hostentry(tmpdir):
    ''' add an ipv4 type entry '''
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost")
    hosts = Hosts(path=hosts_file.strpath)
    hosts_entry = HostsEntry(entry_type='ipv4', address='123.123.123.123', names=['test.example.com'])
    hosts.add(entry=hosts_entry, force=False)
    assert hosts.count(address="123.123.123.123").get('address_matches') == 1
    assert hosts.count(address="127.0.0.1").get('address_matches') == 1

def test_replace_ipv4_host_where_ip_differs(tmpdir):
    ''' replace an ipv4 entry where ip differs '''
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("82.132.132.132\texample.com\texample")
    hosts_entries = Hosts(path=hosts_file.strpath)
    hosts_entries.add(force=True, entry_type='ipv4', address='82.132.132.133', names=['example.com', 'example'])
    counts = hosts_entries.count(address="82.132.132.133")
    assert counts.get('address_matches') == 1

def test_replace_ipv4_host_where_name_differs(tmpdir):
    ''' replace an ipv4 entry where name differs '''
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("82.132.132.132\texample.com\texample")
    hosts_entries = Hosts(path=hosts_file.strpath)
    hosts_entries.add(force=True, entry_type='ipv4', address='82.132.132.132', names=['example2.com', 'example'])
    counts = hosts_entries.count(address="82.132.132.132", names=['example2.com', 'example'])
    assert counts.get('address_matches') == 1 and counts.get('name_matches') == 1

def test_add_single_ipv6_host(tmpdir):
    ''' add a single ipv6 host '''
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost")
    hosts_entries = Hosts(path=hosts_file.strpath)
    hosts_entries.add(force=False, entry_type='ipv6', address='::1', names=['localhost6.localdomain6', 'localhost6'])
    assert hosts_entries.count(address="::1").get('address_matches') == 1

def test_add_single_comment(tmpdir):
    comment = 'this is a comment'
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("")
    hosts_entries = Hosts(path=hosts_file.strpath)
    hosts_entries.add(force=False, entry_type='comment', address=None, comment=comment)
    assert hosts_entries.count(comment=comment).get('comment_matches') == 1

def test_remove_single_comment(tmpdir):
    comment = "#127.0.0.1\tlocalhost"
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write(comment)
    hosts_entries = Hosts(path=hosts_file.strpath)
    hosts_entries.add(HostsEntry({'comment': comment}))
    assert hosts_entries.count(comment=comment).get('comment_matches') == 1
    hosts_entries.remove(passed_comment=comment)
    assert hosts_entries.count(comment=comment).get('comment_matches') == 0