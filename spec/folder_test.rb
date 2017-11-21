title 'OS'

describe directory('/this-test-directory-in-root') do
  it { should be_directory }
end
