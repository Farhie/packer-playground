control "cis-1-1-1-1" do
  impact 1.0
  title "Ensure mounting of cramfs filesystems is disabled (Scored)"
  desc "The cramfs filesystem type is a compressed read-only Linux filesystem
        embedded in small footprint systems. A cramfs image can be used without
        having to first decompress the image."

  describe command('modprobe -n -v cramfs') do
    its('stdout') { should match 'install /bin/true' }
  end

  describe command('lsmod | grep cramfs') do
    its('stdout') { should match '' }
  end

  remediation = file('/etc/modprobe.d/CIS.conf')

  describe remediation do
    it { should exist }
    its ('content') { should include 'install cramfs /bin/true'}
  end
end


control "cis-1-1-1-2" do
  impact 1.0
  title "Ensure mounting of freevxfs filesystems is disabled (Scored)"
  desc "The freevxfs filesystem type is a free version of the Veritas type
        filesystem. This is the primary filesystem type for HP-UX operating systems."

  describe command('modprobe -n -v freevxfs') do
    its('stdout') { should match 'install /bin/true' }
  end

  describe command('lsmod | grep freevxfs') do
    its('stdout') { should match '' }
  end

  remediation = file('/etc/modprobe.d/CIS.conf')

  describe remediation do
    it { should exist }
    its ('content') { should include 'install freevxfs /bin/true'}
  end
end
