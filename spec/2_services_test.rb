control "cis-2.1.1" do
  impact 1.0
  title "Ensure chargen services are not enabled (Scored)"
  desc "chargen is a network service that responds with 0
       to 512 ASCII characters for each connection it receives.
       This service is intended for debugging and testing purposes.
       It is recommended that this service be disabled."

  describe service('chargen-dgram') do
    it { should_not be_installed }
  end

  describe service('chargen-stream') do
    it { should_not be_installed }
  end
end
