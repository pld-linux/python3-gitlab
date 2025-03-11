#
# Conditional build:
%bcond_with		doc	# don't build doc
%bcond_with		tests	# do not perform "make test"

%define 	module		gitlab
%define 	egg_name	python_gitlab
%define		pypi_name	python-gitlab
Summary:	Interact with GitLab API
Name:		python3-gitlab
Version:	3.13.0
Release:	3
License:	LGPLv3
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	b4ffdd18a187a263b9486b27a3576c7e
Source1:	config.cfg
URL:		https://python-gitlab.readthedocs.io
BuildRequires:	python3-devel
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Interact with GitLab API

%prep
%setup -q -n %{pypi_name}-%{version}

# Remove bundled egg-info
%{__rm} -r %{egg_name}.egg-info

%build
%py3_build %{?with_tests:test}

%if %{with doc}
sphinx-build-3 docs html
%{__rm} -r html/.{doctrees,buildinfo}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{_sourcedir}/config.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{pypi_name}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{pypi_name}.cfg
%attr(755,root,root) %{_bindir}/gitlab
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
