// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only capture of a saved AI match through the native strategic interface.
#include "CommandLine.h"
#include "GlobalContainer.h"
#include "GameGUI.h"
#include "Team.h"
#include "Unit.h"
#include "Building.h"
#include "Player.h"
#include "map/io/MapHeader.h"
#include <BinaryStream.h>
#include <Toolkit.h>
#include <SDL3/SDL.h>
#include <fstream>
#include <filesystem>
#include <FileManager.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <stdexcept>
GlobalContainer *globalContainer=nullptr;
static void save(GameGUI& gui,const std::string& path){
 FILE* fp=fopen(path.c_str(),"wb");if(!fp)throw std::runtime_error("Cannot write staged save");
 GAGCore::BinaryOutputStream out(new GAGCore::FileStreamBackend(fp));gui.save(&out,"Marketing skirmish: staged armies, genuine simulation");out.flush();
}
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("usage scene MAP OUTDIR");
 const char* assetDir=std::getenv("GLOB2_MARKETING_ASSET_DIR");if(!assetDir)throw std::runtime_error("Set GLOB2_MARKETING_ASSET_DIR to the game data directory");
 std::string base=argv[2];globalContainer=new GlobalContainer;
 globalContainer->applyCommand(Cli::parse(std::vector<std::string>{"play","--renderer","software","--window-size","1920x1080","--mute","--data-dir",assetDir}));
 globalContainer->settings.mute=1;globalContainer->settings.autosaveGames=false;globalContainer->settings.clouds=false;globalContainer->settings.cloudShadows=false;globalContainer->settings.adaptiveZoomDetail=true;
 globalContainer->load();
 { GameGUI gui;GAGCore::BinaryInputStream in(glob2OpenMapOrSaveInputStreamBackend(*GAGCore::Toolkit::getFileManager(),argv[1]));if(!gui.load(&in,true))throw std::runtime_error("Cannot load native source map");
 gui.localPlayer=gui.localTeamNo=0;gui.adjustLocalTeam();gui.adjustInitialViewport();
 const int W=gui.game.map.getW(),H=gui.game.map.getH();
 int units=0,buildings=0,warriors=0;
 for(int t=0;t<gui.game.mapHeader.getNumberOfTeams();t++) {
  for(int i=0;i<Unit::MAX_COUNT;i++) if(auto*u=gui.game.teams[t]->myUnits[i]) {units++;warriors+=u->typeNum==WARRIOR;}
  for(int i=0;i<Building::MAX_COUNT;i++) if(gui.game.teams[t]->myBuildings[i])buildings++;
 }
 std::cout<<"native saved-state units="<<units<<" warriors="<<warriors<<" buildings="<<buildings<<" map="<<W<<"x"<<H<<std::endl;
 // Native spectator options: no fog concealment in the authored capture.
 globalContainer->liveSpectating=true;globalContainer->replayShowFog=false;globalContainer->replayVisibleTeams=0xffffffff;globalContainer->replayShowAreas=false;globalContainer->replayShowFlags=false;
 gui.configureLiveSpectatorView();
 auto draw=[&](const std::string&name,double zoom,int x,int y){
  gui.camera.zoom=zoom;gui.prepareLocalPresentation();gui.updateCamera();gui.camera.originX=x*32.-gui.camera.visibleW()/2.;gui.camera.originY=y*32.-gui.camera.visibleH()/2.;gui.viewportX=gui.camera.tileX();gui.viewportY=gui.camera.tileY();
  for(int f=0;f<20;f++){SDL_PumpEvents();GAGCore::Toolkit::pollAssets();gui.prepareLocalPresentation();gui.drawAll(0);globalContainer->gfx->nextFrame();SDL_Delay(10);}
  const auto file=std::filesystem::relative(base+"/"+name+".bmp",std::filesystem::absolute(GAGCore::Toolkit::getFileManager()->getDir(0))).string();
  globalContainer->gfx->printScreen(file);gui.prepareLocalPresentation();gui.drawAll(0);globalContainer->gfx->nextFrame();
 };
 const double overview=0.20;
 draw("strategic-candidate",overview,W/4,H/2);

 }
 std::cout<<"done"<<std::endl;return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 1;}}
