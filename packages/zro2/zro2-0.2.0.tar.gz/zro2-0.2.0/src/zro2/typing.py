from typing import TypedDict, get_overloads, get_type_hints
import inspect
import typing

def get_overload_signatures(func):
    overloads = get_overloads(func)
    for overloadFunc in overloads:
        yield inspect.signature(overloadFunc)

def bind_overload(overloadFunc, *args, **kwargs):
    for sig in get_overload_signatures(overloadFunc):
        try:
            return sig.bind(*args, **kwargs).arguments
        except TypeError:
            pass

# Github release typeddict
class GithubAsset(TypedDict):
    url: str
    id: int
    node_id: str
    name: str
    label: str
    content_type: str
    state: str
    size: int
    download_count: int
    browser_download_url: str

class GithubRelease(TypedDict):
    url: str
    assets_url: str
    upload_url: str
    html_url: str
    id: int
    node_id: str
    tag_name: str
    target_commitish: str
    name: str
    draft: bool
    prerelease: bool
    assets: typing.List[GithubAsset]
    tarball_url: str
    zipball_url: str
    body: str

# funcs

def is_valid_typeddict(instance, typeddict: type) -> bool:
    required_keys = {k for k, v in get_type_hints(typeddict).items() if not isinstance(v, type(None))}
    optional_keys = {k for k, v in get_type_hints(typeddict).items() if isinstance(v, type(None))}

    # Check for required keys and correct types
    if not all(k in instance and isinstance(instance[k], get_type_hints(typeddict)[k]) for k in required_keys):
        return False

    # Check for optional keys and correct types if present
    if not all(isinstance(instance[k], get_type_hints(typeddict)[k]) for k in optional_keys if k in instance):
        return False

    # Optionally, ensure no extra keys are present
    all_keys = required_keys.union(optional_keys)
    if not all(k in all_keys for k in instance.keys()):
        return False

    return True