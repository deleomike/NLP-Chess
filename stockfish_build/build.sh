git clone --depth 1 --branch sf_14 git@github.com:official-stockfish/Stockfish.git stockfish
cd stockfish/src
make help
make net
make build ARCH=x86-64-modern