control "cis-1.1.1.1" do
  impact 1.0
  title "Ensure mounting of cramfs filesystems is disabled (Scored)"
  desc "The cramfs filesystem type is a compressed read-only Linux filesystem
        embedded in small footprint systems. A cramfs image can be used without
        having to first decompress the image."

  describe command('lsmod | grep cramfs') do
    its('stdout') { should match '' }
  end
end


control "cis-1.1.1.2" do
  impact 1.0
  title "Ensure mounting of freevxfs filesystems is disabled (Scored)"
  desc "The freevxfs filesystem type is a free version of the Veritas type
        filesystem. This is the primary filesystem type for HP-UX operating systems."

  describe command('lsmod | grep freevxfs') do
    its('stdout') { should match '' }
  end
end

control "cis-1.1.1.3" do
  impact 1.0
  title "Ensure mounting of jffs2 filesystems is disabled (Scored)"
  desc "The jffs2 (journaling flash filesystem 2) filesystem type is a
        log-structured filesystem used in flash memory devices."

  describe command('lsmod | grep jffs2') do
    its('stdout') { should match '' }
  end
end
