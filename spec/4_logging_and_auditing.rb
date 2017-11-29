control "cis-4.1.1.1" do
  impact 1.0
  title "4.1.1.1 Ensure audit log storage size is configured (Not Scored)"
  desc "Configure the maximum size of the audit log file. Once the log reaches the maximum size, it will be rotated
        and a new log file will be started."

  describe auditd_conf do
    its('max_log_file') { should cmp 50 }
  end
end
