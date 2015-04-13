# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from characteristic import attributes
from filepath import FilePath
from mcstatus import MinecraftServer
from nbt.nbt import NBTFile

SERVERS_DAT = "servers.dat"

@attributes(["name", "server"])
class NamedServer(object):
    pass


def server_from_nbt(server_nbt):
    server_address = server_nbt['ip'].value
    name = server_nbt['name'].value
    server = MinecraftServer.lookup(server_address)
    named_server = NamedServer(name=name, server=server)
    return named_server


def main(argv):
    minecraft_dir = FilePath(argv[1])
    assert minecraft_dir.isdir(), minecraft_dir
    servers_filename = minecraft_dir.child(SERVERS_DAT)
    servers = get_servers(servers_filename)

    for server in servers:
        status = server.server.status()
        show_server_players(server, status)

    return 0


def show_server_players(server, status):
    print("%s, %s players" % (server.name, status.players.online))
    if status.players.sample:
        player_names = [player.name for player in status.players.sample]
        for name in player_names:
            print("* %s" % (name,))


def get_servers(servers_filename):
    assert servers_filename.exists()
    with servers_filename.open() as servers_file:
        # `buffer` instead of `fileobj` because NBTFile assumes fileobj is gzipped
        servers_nbt = NBTFile(buffer=servers_file)
        server_defs = servers_nbt['servers']
        servers = [server_from_nbt(server) for server in server_defs]
    return servers


if __name__ == '__main__':
    exit_code = main(sys.argv)
    raise SystemExit(exit_code)
