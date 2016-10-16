#
# Conditional build:
%bcond_with		doc	# don't build doc
%bcond_with		tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module		gitlab
%define 	egg_name	python_gitlab
%define		pypi_name	python-gitlab
Summary:	Interact with GitLab API
Name:		python-gitlab
Version:	0.16
Release:	1
License:	LGPLv3
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	e0421d930718021e7d796d74d2ad7194
URL:		https://github.com/gpocentek/python-gitlab
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	sphinx-pdg
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Interact with GitLab API

%package -n python3-gitlab
Summary:	Interact with GitLab API
Group:		Libraries/Python

%description -n python3-gitlab
Interact with GitLab API

%prep
%setup -q

# Remove bundled egg-info
%{__rm} -r %{module}.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
sphinx-build-2 docs html
%{__rm} -r html/.{doctrees,buildinfo}
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with doc}
sphinx-build-3 docs html
%{__rm} -r html/.{doctrees,buildinfo}
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
mv $RPM_BUILD_ROOT%{_bindir}/gitlab $RPM_BUILD_ROOT%{_bindir}/gitlab-2
%endif

%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/gitlab $RPM_BUILD_ROOT%{_bindir}/gitlab-3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/gitlab-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-gitlab
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/gitlab-3
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
