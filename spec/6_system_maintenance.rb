control "cis-6.1" do
  impact 1.0
  title "6.1.2 Ensure permissions on /etc/passwd are configured (Scored)"
  desc "The /etc/passwd file contains user account information that is used by many system utilities and therefore
        must be readable for these utilities to operate."

  describe file('/etc/passwd') do
    it { should be_owned_by 'root' }
    it { should be_setuid }
    it { should be_setgid }
  end
end
