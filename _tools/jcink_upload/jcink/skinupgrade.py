import logging
log = logging.getLogger("upgrade")
import subprocess
import re
from .skinmanager import SkinManager
from .filemanager import FileManager

skin_name_regex = re.compile(r"^(?P<skin>just-the-docs) (?P<variant>dark|light|default) (?P<version>.*)$")

def find_candidate_upgrade(ver:str, obsolete:list[str]=[]):
    cmd = ["git", "describe", "--always", "--contains", "--tags"]
    for obver in obsolete:
        cmd.extend(["--exclude", obver])
    cmd.append(ver)
    return subprocess.run(cmd, capture_output=True).stdout.decode().strip().split("~",1)[0].split("^",1)[0]

def calc_upgrade_path(skin_matches:list[re.Match], obsolete:list[str]=[]) -> tuple[dict[str,str], set[str]]:
    '''
    :param obsolete: list of tags that should be discarded even if good
    :return 0: dictionary of upgrades to make
    :return 1: set of version hashes whose last member will be removed by this update
    '''
    upgrade_path = {}
    versions = set()

    for m in skin_matches:
        info = m.groupdict()

        info["upgrade"] = find_candidate_upgrade(info["version"], obsolete=obsolete)
        
        original = "{skin!s} {variant!s} {version!s}".format(**info)
        upgraded = "{skin!s} {variant!s} {upgrade!s}".format(**info)
        upgrade_path[original] = upgraded
        
        versions.add(original) # just collecting for now, we'll drop versions later

    begin_hashes = {
        skin_name_regex.match(v).group("version") for v in versions
    }

    # Remove upgrades to versions that aren't available on the site.
    some_deleted = True
    while some_deleted:
        some_deleted = False
        for k,v in list(upgrade_path.items()):
            if v not in upgrade_path:
                log.warning("can't find target: %s => %s", k, v)
                del upgrade_path[k]
                some_deleted = True

    # Remove upgrades from a version to itself.
    for k,v in list(upgrade_path.items()):
        if k == v:
            del upgrade_path[k]
    
    some_modified = True
    while some_modified:
        some_modified = False
        for v in list(versions):
            if v in upgrade_path:
                versions.pop(v)
                versions.push(upgrade_path[v])
                some_modified = True
    
    end_hashes = {
        skin_name_regex.match(v).group("version") for v in versions
    }

    return upgrade_path, (begin_hashes - end_hashes)

def upgrade_all_skins(sm: SkinManager, fm: FileManager, pattern:re.Pattern, obsolete:list[str]=[], dry_run=False, cleanup=True):
    skins = sm.list_skins(pattern)
    upgrade_path, del_hashes = calc_upgrade_path(skins, obsolete=obsolete)

    for k,v in upgrade_path.items():
        log.info("%s => %s", k, v)
        sm.upgrade_skin(k, v, dry_run=dry_run)
        sm.delete_skin(k, dry_run=dry_run)

    if cleanup:
        sm.cleanup()
    else:
        log.warning("not cleaning up skin components")
        
    for h in del_hashes:
        assets_path = f"/assets_{h}"
        if cleanup:
            log.info("remove %s", assets_path)
            fm.rm_contents(assets_path, dry_run=dry_run)
            fm.rm(assets_path, dry_run=dry_run)
        else:
            log.warning("not cleaning up %s", assets_path)


