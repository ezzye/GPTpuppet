# Go to the home directory
# The home directory is /content/planning

# Remove any previously downloaded zip files to avoid .1 suffix and re-download the ChromeDriver zip file
rm -f chromedriver_linux64.zip*
rm -f chromedriver-linux64.zip*
rm -rf chromedriver_extracted*

wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip


# Unzip the ChromeDriver zip file with -o option to overwrite without prompting
unzip -o chromedriver-linux64.zip -d chromedriver_extracted

# Move the ChromeDriver to '/usr/local/bin/' and set the executable permissions
sudo mv /content/planning/chromedriver_extracted/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
