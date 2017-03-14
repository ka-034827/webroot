  # List packages required to be installed for this demo: 
  environment.systemPackages = with pkgs; [
     git
     which
     python27
     python27Packages.flask
     python27Packages.pip
     sqlite
   ];

  # List service that needs to be disabled for this demo:
  networking.firewall.enable = false;
