%global pkg_name tycho-extras
%{?scl:%scl_package %{pkg_name}}
# When building version under development (non-release)
# %%global snap -SNAPSHOT
%global snap %{nil}

Name:           %{?scl_prefix}tycho-extras
Version:        0.22.0
Release:        4.bootstrap1%{?dist}
Summary:        Additional plugins for Tycho

License:        EPL
URL:            http://eclipse.org/tycho/
Source0:        http://git.eclipse.org/c/tycho/org.eclipse.tycho.extras.git/snapshot/org.eclipse.tycho.extras-tycho-extras-0.22.0.tar.bz2
Patch0:         %{pkg_name}-fix-build.patch
Patch1:         %{pkg_name}-use-custom-resolver.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}jgit
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}tycho >= 0.22.0-3

Requires:  %{?scl_prefix}jgit
Requires:  %{?scl_prefix}tycho >= 0.22.0-3

%description
A small set of plugins that work with Tycho to provide additional functionality
when building projects of an OSGi nature.


%package javadoc
Summary:        Java docs for %{pkg_name}
Group:          Documentation

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n org.eclipse.tycho.extras-tycho-extras-0.22.0
%patch0 -p1
%patch1 -p1

%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl_maven} %{scl} - << "EOF"}
# maven-properties-plugin is only needed for tests
%pom_remove_plugin org.eclipse.m2e:lifecycle-mapping
%pom_remove_plugin org.sonatype.plugins:maven-properties-plugin tycho-p2-extras-plugin
# remove org.apache.maven:apache-maven zip
%pom_remove_dep org.apache.maven:apache-maven tycho-p2-extras-plugin

%mvn_alias :{*} org.eclipse.tycho:@1
%{?scl:EOF}

%build
# To run tests, we need :
# maven-properties-plugin (unclear licensing)
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl_maven} %{scl} - << "EOF"}
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc

%changelog
* Mon Apr 27 2015 Mat Booth <mat.booth@redhat.com> - 0.22.0-4
- Related: rhbz#1184224 - Bump release and rebuild

* Fri Jan 09 2015 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-3
- Add explicit Requires and disable auto-prov/req generation.

* Tue Jan 06 2015 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-2.1
- SCL-ize.
- Related: rhbz#1175105

* Fri Dec  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-2
- Port to latest fedoraproject-p2

* Mon Dec 01 2014 Mat Booth <mat.booth@redhat.com> - 0.22.0-1
- Update to tagged release
- Fix directory ownership problem

* Tue Nov 25 2014 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-0.1.gitef068a
- Update to 0.22.0 pre-release.

* Wed Sep 03 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-3
- Use fedoraproject-p2 to do OSGi bundle discovery.

* Thu Aug 21 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-2
- Integrate fedoraproject-p2 functionality.

* Fri Jul 25 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-1
- Update to 0.21.0 Release.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-1
- Update to 0.20.0 Release.

* Tue Mar 11 2014 Michael Simacek <msimacek@redhat.com> - 0.19.0-3
- Use mvn_build and mvn_install.
- Drop manual requires.

* Thu Feb 27 2014 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-2
- Change R:java to R:java-headless (Bug 1068575).

* Fri Oct 25 2013 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-1
- Update to 0.19.0 Release.

* Mon Jul 29 2013 Roland Grunberg <rgrunber@redhat.com> 0.18.1-1
- Update to 0.18.1 Release.

* Thu May 30 2013 Roland Grunberg <rgrunber@redhat.com> 0.18.0-1
- Update to 0.18.0 Release.

* Tue May 7 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-2
- tycho-eclipserun-plugin should use the system local p2 repo.

* Tue Apr 2 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-1
- Update to 0.17.0 Release.

* Mon Feb 25 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-0.1.git0a9370
- Update to latest 0.17.0-SNAPSHOT.

* Thu Feb 21 2013 Roland Grunberg <rgrunber@redhat.com> - 0.16.0-5
- Fix PlexusConfiguration class issues identically across branches.

* Wed Feb 20 2013 Roland Grunberg <rgrunber@redhat.com> - 0.16.0-4
- Fix build issues relating to PlexusConfiguration.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-3
- Fix upstream Bug 393686.

* Fri Oct 19 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-2
- Update to 0.16.0 Release.

* Mon Jul 30 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-1.e58861
- Update to 0.16.0 SNAPSHOT.

* Fri Jul 27 2012 Roland Grunberg <rgrunber@redhat.com> 0.15.0-1
- Update to 0.15.0.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Roland Grunberg <rgrunber@redhat.com> - 0.14.0-1
- Initial packaging of tycho extras.
