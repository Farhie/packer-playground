control "cis-3-1-1" do
  impact 1.0
  title "Ensure IP forwarding is disabled (Scored)"
  desc "The net.ipv4.ip_forward flag is used to tell the system whether
        it can forward packets or not"

  describe command('sysctl net.ipv4.ip_forward') do
    its('stdout') { should match 'net.ipv4.ip_forward = 0' }
  end


  describe kernel_parameter('net.ipv4.ip_forward') do
    its('value') { should eq 0 }
  end

  describe kernel_parameter('net.ipv4.route.flush') do
    its('value') { should eq 1 }
  end

  remediation = file('/etc/sysctl.conf')

  describe remediation do
    it { should exist }
    its ('content') { should include 'net.ipv4.ip_forward = 0'}
  end
end
