control "cis-5.1" do
  impact 1.0
  title "5.1.1 Ensure cron daemon is enabled (Scored)"
  desc "The cron daemon is used to execute batch jobs on the system."

  describe service('crond').runlevels(2,3,4,5) do
    it { should be_enabled }
  end

  describe service('crond').runlevels(0,1,6) do
    it { should_not be_enabled }
  end
end
