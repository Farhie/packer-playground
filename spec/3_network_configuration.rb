control "cis-3.1.1" do
  impact 1.0
  title "Ensure IP forwarding is disabled (Scored)"
  desc "The net.ipv4.ip_forward flag is used to tell the system whether
        it can forward packets or not"

  describe kernel_parameter('net.ipv4.ip_forward') do
    its('value') { should eq 0 }
  end
end


control "cis-3.1.2" do
  impact 1.0
  title "3.1.2 Ensure packet redirect sending is disabled (Scored)"
  desc "ICMP Redirects are used to send routing information to other hosts. As a host itself does not act as a router
        (in a host only configuration), there is no need to send redirects."

  describe kernel_parameter('net.ipv4.conf.all.send_redirects') do
    its('value') { should eq 0 }
  end

  describe kernel_parameter('net.ipv4.conf.default.send_redirects') do
    its('value') { should eq 0 }
  end
end
