## TAKProto 3.0.0

Happy Summer Solstice!

- Fixes #15: Time data from iTak not parsed.
- Fixes #12: Add CHANGELOG
- Fixes #19: Support timestamps without microseconds. Thanks @sei-jmattson
- Fixes #17/#18: Support mixed-mode rx. Thanks @sei-jmattson
- Fixes #16: Fix datetime parsing for newer TAK clients that don't include microseconds in the timestamp. Thanks @brian7704
- Rewrote GitHub actions, moved most logic to shell script and Makefile.
- Renamed Debian package from python3-takproto to takproto.
- Standardized Makefile for all PyTAK based programs.
- Cleaned, simplified and expanded documentation.
- Created Makefile jobs for Debian packaging and TAKProto customization.
- Moved all media to media sub directory under docs/.
- Converted README.rst to README.md.
- Style & Linting of code.

## TAKProto 2.1.1

- Fixes #12: Add Changelog.  
- Fixes #13: Missing Proto dir?
- Fixes #14: Don't throw away ImportError in __init__.py

## TAKProto 2.1.0

- Fixes #6: Fix xmlDetail compostion (include all details). Thanks @sei-jmattson!
- Fixes #7: CoT Time/Start/Stale timestamps aren't actually ISO-8601.
- Fixes #8: Add readthedocs documentation site.
- Fixes #9: Move setup.py metadata to setup.cfg
- Fixes #10: Add additional test targets: Python 3.11 & 3.12
- Fixes #11: Python 3.6 Build Fails.
- Fixes #12: Add CHANGELOG.
- Documentation Updates.
- Linting & Style.

## TAKProto 2.0.0

- Documentation Updates.
- Fixed example error and problem encoding xmldetail.
- Rewrite to add support for mesh & stream formats.
- Fixes #3: parse_proto in README is inaccurate. Thanks @sei-jmattson!
- Fixes #2: Include generated protobuf folder in the install. Thanks @shelbydavis!

## TAKProto 1.0.2

Documentation updates.

## TAKProto 1.0.1

Documentation updates.

## TAKProto 1.0.0

Initial public release of re-write by @ampledata

## takprotobuf 0.0.1

Initial public release from @dB-SPL