# Third-party code and license notes

The TPAP v2 transport is not an original implementation in this repository.
Source: https://github.com/ZeliardM/python-kasa
Upstream pull request: https://github.com/python-kasa/python-kasa/pull/1592
Pinned commit: `e7084472972f08f2e2235b342f3964aedbfaeb3b`

The vendoring process rewrites Python absolute imports from `kasa` to a private
module namespace `custom_components.tapo_tpap._vendor.kasa`, and replaces
the upstream module version lookup. Those transformed files remain licensed
under the original project's GPL-3.0-or-later license and preserve its LICENSE.

Our new HACS integration code is separately maintained under this repository's
license, subject to the upstream GPL redistribution obligations when packaged.
