%global pkg_name tycho-extras
%{?scl:%scl_package %{pkg_name}}
# If Eclipse not in buildroot, then JGit not in buildroot
# In this case set the bootstrap flag
%global bootstrap 0
# When building version under development (non-release)
# %%global snap -SNAPSHOT
%global snap %{nil}

Name:           %{?scl_prefix}tycho-extras
Version:        0.23.0
Release:        2.2%{?dist}
Summary:        Additional plugins for Tycho

License:        EPL
URL:            http://eclipse.org/tycho/
Source0:        http://git.eclipse.org/c/tycho/org.eclipse.tycho.extras.git/snapshot/org.eclipse.tycho.extras-tycho-extras-%{version}.tar.xz
Patch0:         %{pkg_name}-fix-build.patch
Patch1:         %{pkg_name}-use-custom-resolver.patch
Patch2:         0001-Update-to-JGit-4.0.patch

BuildArch:      noarch

%if ! %{bootstrap}
BuildRequires:  %{?scl_prefix}jgit
%endif
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}tycho >= 0.22.0-3

%if ! %{bootstrap}
Requires:       %{?scl_prefix}jgit
%endif
Requires:       %{?scl_prefix}tycho >= 0.22.0-3


%description
A small set of plugins that work with Tycho to provide additional functionality
when building projects of an OSGi nature.


%package javadoc
Summary:        Java docs for %{pkg_name}
Group:          Documentation

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n org.eclipse.tycho.extras-tycho-extras-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# maven-properties-plugin is only needed for tests
%pom_remove_plugin org.eclipse.m2e:lifecycle-mapping
%pom_remove_plugin org.sonatype.plugins:maven-properties-plugin tycho-p2-extras-plugin
# remove org.apache.maven:apache-maven zip
%pom_remove_dep org.apache.maven:apache-maven tycho-p2-extras-plugin
%pom_add_dep org.fedoraproject.p2:org.fedoraproject.p2 tycho-eclipserun-plugin/pom.xml

%mvn_alias :{*} org.eclipse.tycho:@1

%if %{bootstrap}
%pom_disable_module tycho-sourceref-jgit
%pom_disable_module tycho-buildtimestamp-jgit
%endif

%{?scl:EOF}

%build
# To run tests, we need :
# maven-properties-plugin (unclear licensing)
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Jun 30 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-2.2
- Non bootstrap build

* Sun Jun 28 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-2.1
- SCL-ize.
- Re-introduce a bootstrap mode to avoid jgit dependency.

* Sun Jun 28 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-2.1
- Initial import of tycho-extras-0.23.0-2.fc23.
