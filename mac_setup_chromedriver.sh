# Remove any previously downloaded zip files to avoid .1 suffix and re-download the ChromeDriver zip file
rm -f chromedriver-linux64.zip*
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/mac-x64/chromedriver-mac-x64.zip

# Unzip the ChromeDriver zip file with -o option to overwrite without prompting
unzip -o chromedriver-mac-x64.zip -d chromedriver_extracted

# Move the ChromeDriver to '/usr/local/bin/' and set the executable permissions
mv chromedriver_extracted/chromedriver-mac-x64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
