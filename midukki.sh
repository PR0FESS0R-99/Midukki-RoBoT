if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/PR0FESS0R-99/Midukki-RoBoT.git /Midukki-RoBoT
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Midukki-RoBoT
fi
cd /Midukki-RoBoT
pip3 install -U -r requirements.txt
echo "Starting Midukki-RoBot...."
python3 -m Midukki
