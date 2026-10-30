# The tarball contains odd named directory; use variables to make %%prep work
%global dir_name oscar-sql

Name:           oscar20
Version:        2.1.0
Release:        1%{?dist}
Summary:        Open Source CPAP Analysis Reporter
# Main code is GPL-3.0-only; bundled botan is BSD-2-Clause, bundled miniz is MIT
License:        GPL-3.0-only AND BSD-2-Clause AND MIT
URL:            https://sleepfiles.com/OSCAR
# The source of this package was pulled from upstreams's vcs.
# Use the following command to generate the tar ball:
# git clone https://gitlab.com/CrimsonNape/OSCAR-SQL.git oscar-sql-v<version>
# tar cvjf oscar-sql-v<version>.tar.bz2 oscar-sql-v<version>/
Source0:        oscar-sql-v%{version}.tar.bz2

# Upstream provides none of the following files
Source1:        org.oscar-team.OSCAR20.desktop
Source2:        OSCAR20.1
Source3:        org.oscar-team.OSCAR20.metainfo.xml

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtserialport-devel
BuildRequires:  qt6-linguist

BuildRequires:  zlib-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libX11-devel

BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils

Provides:       bundled(botan2)
Provides:       bundled(miniz)

%description
OpenSource CPAP Analysis Reporter - OSCAR
OSCAR is a derivative of SleepyHead version 1.1.0, created when that was
abandoned by Mark Watkins.
SleepyHead was a cross platform, open source sleep tracking program for
reviewing CPAP and Oximetry data, which are devices used in the treatment of
Sleep Disorders like Obstructive Sleep Apnea. It was released under the GPL
version 3 license. See the file COPYING for those details.
SleepyHead was written by Mark Watkins (aka Jedimark), an Australian software
developer afflicted with sleep apnea.

%prep
%autosetup -n %{dir_name}-v%{version}
# Upstream builds with -Werror, which breaks with every new compiler and with
# the distribution's hardening flags; warnings are not errors in a distro build
sed -i '/^QMAKE_C\(XX\)\?FLAGS += -Werror$/d' oscar/oscar.pro

%build
mkdir build
cd build
%qmake_qt6 ../OSCAR_QT.pro
%make_build

%install
install -Dm 0755 build/oscar/OSCAR20 %{buildroot}%{_bindir}/OSCAR20

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_metainfodir}/org.oscar-team.OSCAR20.metainfo.xml

install -Dpm 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/OSCAR20.1

# install icons
for size in 32 48 64 128 256 512; do
install -Dpm 0644 Building/Icons/Full-${size}.png                             \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/OSCAR20.png
done
install -Dpm 0644 Building/Linux/OSCAR20.svg                                 \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/OSCAR20.svg

install -d %{buildroot}%{_datadir}/OSCAR20/Translations
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR20/Translations/ oscar/translations/*.qm
install -d %{buildroot}%{_datadir}/OSCAR20/Html
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR20/Html/ build/oscar/Html/*

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.oscar-team.OSCAR20.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.oscar-team.OSCAR20.metainfo.xml

%files
%license COPYING
%doc README
%{_bindir}/OSCAR20
%{_datadir}/applications/org.oscar-team.OSCAR20.desktop
%{_metainfodir}/org.oscar-team.OSCAR20.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/OSCAR20.png
%{_datadir}/icons/hicolor/scalable/apps/OSCAR20.svg
%{_datadir}/OSCAR20/
%{_mandir}/man1/OSCAR20.1*


%changelog
* Wed Oct 28 2026 Johan Heikkila <johan.heikkila@gmail.com> - 2.1.0-1
- OSCAR 2.1
- Build with distribution compiler flags, enable debuginfo
- Drop upstream -Werror
- Drop unused help files, fix icon sizes, add AppStream metadata
* Tue Jun 30 2026 Johan Heikkila <johan.heikkila@gmail.com> - 2.0.1-1
- Initial package of OSCAR 2.x
- Package renamed to oscar20 to allow parallel installation with oscar 1.x
- Update to upstream SQL backend release 2.0.1
