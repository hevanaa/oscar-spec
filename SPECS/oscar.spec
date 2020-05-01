%global debug_package %{nil}
# The tarball contains odd named directory; use variables to make %prep work
%global g_version 1.1.0
%global g_release 1
%global dir_name OSCAR-code

Name:           oscar
Version:        %{g_version}
Release:        %{g_release}%{?dist}
Summary:        Open Sourece CPAP Analysis Reporter
Group:          Applications/Engineering
License:        GPLv3
URL:            https://sleepfiles.com/OSCAR
# The source of this package was pulled from upstreams's vcs.
# Use the following command to generate the tar ball:
# git clone https://gitlab.com/pholy/OSCAR-code.git
# tar cvjf OSCAR-code-v%{g_version}.tar.bz2 oscar-code/
Source0:        OSCAR-code-v%{g_version}.tar.bz2

# Upstream provides none of the following files
Source1:        OSCAR.desktop
Source2:        OSCAR.appdata.xml
Source3:        OSCAR.1

# Required for Fedora 32
Patch0:         0001-avoid_int-in-bool-context_error.patch

BuildRequires:  qt5-qtwebkit-devel >= 5.9.0
BuildRequires:  qt5-qtserialport-devel >= 5.9.0
BuildRequires:  qt5-qttools-devel >= 5.9.0
%if 0%{?fedora}%{?el8}
BuildRequires:  quazip-qt5-devel
%endif
%if 0%{?el7}
BuildRequires:  quazip-devel
%endif
BuildRequires:  zlib-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libX11-devel
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel

BuildRequires:  qt5-linguist
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick

Requires:       qt5-qtwebkit >= 5.9.0
Requires:       qt5-qtserialport >= 5.9.0

%description
OpenSource CPAP Analysis Reporter - OSCAR
OSCAR is a derivative of SleepyHead version 1.1.0,created when that was
abandoned by Mark Watkins.
SleepyHead was a cross platform, opensource sleep tracking program for reviewing
CPAP and Oximetry data, which are devices used in the treatment of Sleep
Disorders like Obstructive Sleep Apnea. It was released under the GPL version 3
license. See the file COPYING for those details.
SleepyHead was written by Mark Watkins (aka Jedimark), an Australian software
developer afflicted with sleep apnea.

%prep
%setup -q -n %{dir_name}-v%{g_version}

%patch0 -p0

%build
mkdir build
cd build
%if 0%{?rhel}
qmake-qt5 QMAKE_CXXFLAGS+=-Wno-error=unused-parameter QMAKE_CFLAGS+=-Wno-error=strict-aliasing ../OSCAR_QT.pro
%endif
%if 0%{?fedora}
qmake-qt5 ../OSCAR_QT.pro
%endif
make %{?_smp_mflags}

# Convert icon sizes to freedesktop standard
mogrify -resize 96x96 ../oscar/icons/logo-lm.png
mogrify -resize 256x256 ../oscar/icons/logo-lg.png

%install
install -Dm 0755 build/oscar/OSCAR $RPM_BUILD_ROOT%{_bindir}/OSCAR

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

install -Dpm 0644                                                             \
%{SOURCE2} %{buildroot}%{_datadir}/appdata/OSCAR.appdata.xml
appstream-util                                                                \
validate-relax --nonet %{buildroot}%{_datadir}/appdata/OSCAR.appdata.xml

install -Dpm 0644 %{SOURCE3} %{buildroot}%{_mandir}/man1/OSCAR.1

# install icons
num=( 1 2 3 4 )
name=( sm md lm lg )
pxl=( 24 64 96 256 )
for (( i=0; i<${#num[@]}; i++ )); do
install -Dpm 0644                                                             \
oscar/icons/logo-${name[$i]}.png             \
%{buildroot}%{_datadir}/icons/hicolor/${pxl[$i]}x${pxl[$i]}/apps/OSCAR.png
done

install -d %{buildroot}%{_datadir}/OSCAR/Translations
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR/Translations/ oscar/translations/*.qm
install -d %{buildroot}%{_datadir}/OSCAR/Html
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR/Html/ build/oscar/Html/*
install -d %{buildroot}%{_datadir}/OSCAR/Help
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR/Help/ oscar/help/index.qhcp
install -d %{buildroot}%{_datadir}/OSCAR/Help/help_en
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR/Help/ oscar/help/help_en/*
install -d %{buildroot}%{_datadir}/OSCAR/Help/help_nl
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR/Help/ oscar/help/help_nl/*
install -d %{buildroot}%{_datadir}/OSCAR/Help/images
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/OSCAR/Help/ oscar/help/images/*

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :


%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license COPYING
%doc README
%{_bindir}/*
%{_datadir}/applications/OSCAR.desktop
%{_datadir}/appdata/OSCAR.appdata.xml
%{_datadir}/icons/hicolor/*/apps/OSCAR.png
%{_datadir}/OSCAR/
%{_mandir}/man1/OSCAR.1*



%changelog
* Fri May 1 2020 Johan Heikkila <johan.heikkila@gmail.com> - 1.1.0-1
- OSCAR 1.1.0 release

* Thu Apr 25 2019 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.1-1
- Initial script created from sleepyhead
