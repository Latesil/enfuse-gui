%global uuid    com.github.Latesil.%{name}

Name:           enfuse-gui
Version:        0.1.0
Release:        1%{?dist}
Summary:        Simple gui for enfuse script

License:        GPLv3+
URL:            https://gitlab.com/Latesil/enfuse-gui
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(gtk+-3.0)
Requires:       hicolor-icon-theme
Requires:       enblend

%description
%{summary}.


%prep
%autosetup -n %{name}-v%{version} -p1


%build
%meson
%meson_build


%install
%meson_install
%find_lang %{uuid}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{uuid}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/symbolic/*/*.svg
%{_metainfodir}/*.xml


%changelog

* Thu Feb 20 2020 Latesil <vihilantes@gmail.com> - 0.1.0-1
- Initial package

