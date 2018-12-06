# Run tests in check section
%bcond_without check

%global goipath         golang.org/x/perf
%global forgeurl        https://github.com/golang/perf
%global commit          2ce0818a26175593d58f0f5ddb67631b9918296b

%global common_description %{expand:
This subrepository holds the source for various packages and tools related 
to performance measurement, storage, and analysis.

 - cmd/benchstat contains a command-line tool that computes and 7
 compares statistics about benchmarks.
 - cmd/benchsave contains a command-line tool for publishing benchmark
 results.
 - storage contains the https://perfdata.golang.org/ benchmark result 
 storage system.
 - analysis contains the https://perf.golang.org/ benchmark result analysis 
 system.}

%gometa

Name:           %{goname}
Version:        0
Release:        0.3%{?dist}
Summary:        Performance measurement, storage, and analysis
License:        BSD
URL:            %{gourl}
Source0:        %{gosource}

#BuildRequires: golang(github.com/GoogleCloudPlatform/cloudsql-proxy/proxy/dialers/mysql)
BuildRequires: golang(github.com/aclements/go-gg/generic/slice)
BuildRequires: golang(github.com/aclements/go-gg/ggstat)
BuildRequires: golang(github.com/aclements/go-gg/table)
BuildRequires: golang(github.com/go-sql-driver/mysql)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/context/ctxhttp)
BuildRequires: golang(google.golang.org/api/oauth2/v2)
BuildRequires: golang(google.golang.org/appengine)
BuildRequires: golang(google.golang.org/appengine/log)
BuildRequires: golang(google.golang.org/appengine/urlfetch)
BuildRequires: golang(google.golang.org/appengine/user)

%description
%{common_description}


%package devel
Summary:       %{summary}
BuildArch:     noarch

%description devel
%{common_description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.


%prep
%forgeautosetup


%build 
%gobuildroot
for cmd in $(ls -1 cmd) ; do
   %gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done


%install
%goinstall
for cmd in $(ls -1 _bin) ; do
  install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done


%if %{with check}
%check
# Test failure or s390x
# https://github.com/golang/go/issues/26477
%gochecks -d internal/stats
%endif


%files
%license LICENSE PATENTS
%{_bindir}/*


%files devel -f devel.file-list
%license LICENSE PATENTS
%doc README.md CONTRIBUTORS CONTRIBUTING.md AUTHORS


%changelog
* Thu Jul 19 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.3-20180422git2ce0818
- Disable a test that fails on s390x

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.2.git2ce0818
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 22 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.1-20180422git2ce0818
- First package for Fedora

