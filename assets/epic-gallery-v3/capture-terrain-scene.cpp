// SPDX-License-Identifier: GPL-3.0-or-later
// Terrain framing variant of the authored native marketing skirmish; 2026-10-30.
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
 globalContainer->settings.mute=1;globalContainer->settings.autosaveGames=false;globalContainer->settings.clouds=false;globalContainer->settings.cloudShadows=false;globalContainer->settings.adaptiveZoomDetail=false;
 globalContainer->load();
 { GameGUI gui;GAGCore::BinaryInputStream in(glob2OpenMapOrSaveInputStreamBackend(*GAGCore::Toolkit::getFileManager(),argv[1]));if(!gui.load(&in,true))throw std::runtime_error("Cannot load native source map");
 int teams=gui.game.mapHeader.getNumberOfTeams();GameHeader header;header.setRandomSeed(713);header.setNumberOfPlayers(teams);
 for(int t=0;t<teams;t++)header.getBasePlayer(t)=BasePlayer(t,"Colony",t,BasePlayer::P_LOCAL);
 gui.game.setGameHeader(header,false);gui.localPlayer=gui.localTeamNo=0;gui.adjustLocalTeam();gui.adjustInitialViewport();
 int stagedBuildings=0,stagedWorkers=0;
 for(int t=0;t<teams;t++){
  auto* team=gui.game.teams[t];
  for(const char* name:{"inn","school","racetrack","hospital"}){
   int type=globalContainer->buildingsTypes.getFinishedTypeNum(name);if(type<0)throw std::runtime_error("Missing colony building");
   bool placed=false;
   for(int radius=4;radius<18&&!placed;radius++)for(int y=-radius;y<=radius&&!placed;y++)for(int x=-radius;x<=radius&&!placed;x++){
    if(std::max(std::abs(x),std::abs(y))!=radius)continue;
    const auto* bt=globalContainer->buildingsTypes.get(type);
    int bx=(team->startPosX+x)&(gui.game.map.getW()-1),by=(team->startPosY+y)&(gui.game.map.getH()-1);
    if(gui.game.map.isFreeForBuilding(bx,by,bt->width,bt->height))if(auto*b=gui.game.addBuilding(bx,by,type,t)){placed=true;stagedBuildings++;}
   }
   if(!placed)throw std::runtime_error("Native economic cluster could not fit");
  }
  int count=0;
  for(int radius=3;radius<18&&count<24;radius++)for(int y=-radius;y<=radius&&count<24;y++)for(int x=-radius;x<=radius&&count<24;x++){
   if(std::max(std::abs(x),std::abs(y))!=radius)continue;
   int ux=(team->startPosX+x)&(gui.game.map.getW()-1),uy=(team->startPosY+y)&(gui.game.map.getH()-1);
   if(gui.game.map.isGrass(ux,uy)&&gui.game.map.isFreeForGroundUnitNoForbidden(ux,uy,false))if(gui.game.addUnit(ux,uy,t,WORKER,0,0,0,0)){count++;stagedWorkers++;}
  }
 }
 std::cout<<"staged economic buildings="<<stagedBuildings<<" workers="<<stagedWorkers<<std::endl;
 int cx=-1,cy=-1;double score=1e30;const int W=gui.game.map.getW(),H=gui.game.map.getH();
 for(int y=20;y<H-20;y++)for(int x=20;x<W-20;x++){
  double s=std::pow(x-W*.66,2)+std::pow(y-H*.42,2);if(s>=score)continue;bool ok=true;
  for(int dy=-8;dy<=8&&ok;dy++)for(int dx=-16;dx<=16;dx++)if(!gui.game.map.isGrass(x+dx,y+dy)||!gui.game.map.isFreeForGroundUnitNoForbidden(x+dx,y+dy,false)){ok=false;break;}
  if(ok){cx=x;cy=y;score=s;}
 }
 if(cx<0)throw std::runtime_error("No legal open native battle site");
 gui.game.teams[0]->allies=1;gui.game.teams[0]->enemies=2;gui.game.teams[1]->allies=2;gui.game.teams[1]->enemies=1;
 std::vector<Unit*> added;
 for(int t=0;t<2;t++)for(int y=-6;y<6;y++)for(int x=0;x<8;x++){
  int px=cx+(t?6+x:-13+x);auto*u=gui.game.addUnit(px,cy+y,t,WARRIOR,1,0,0,0);if(!u)throw std::runtime_error("Legal native warrior placement failed");added.push_back(u);
 }
 const int flagType=gui.game.buildingsTypes.getTypeNum("warflag",0,false);
 for(int t=0;t<2;t++){
  auto*b=gui.game.addBuilding(cx+(t?-2:2),cy,flagType,t);if(!b)throw std::runtime_error("Native war flag placement failed");
  b->unitStayRange=20;b->maxUnitWorking=96;b->maxUnitWorkingPreferred=96;b->owner->addToStaticAbilitiesLists(b);b->update();
 }
 // Native spectator options: no fog concealment in the authored capture.
 globalContainer->liveSpectating=true;globalContainer->replayShowFog=false;globalContainer->replayVisibleTeams=0xffffffff;globalContainer->replayShowAreas=false;globalContainer->replayShowFlags=false;
 gui.configureLiveSpectatorView();
 auto draw=[&](const std::string&name,double zoom,int x,int y){
  gui.camera.zoom=zoom;gui.prepareLocalPresentation();gui.updateCamera();gui.camera.originX=x*32.-gui.camera.visibleW()/2.;gui.camera.originY=y*32.-gui.camera.visibleH()/2.;gui.viewportX=gui.camera.tileX();gui.viewportY=gui.camera.tileY();
  for(int f=0;f<20;f++){SDL_PumpEvents();GAGCore::Toolkit::pollAssets();gui.prepareLocalPresentation();gui.drawAll(0);globalContainer->gfx->nextFrame();SDL_Delay(10);}
  const auto file=std::filesystem::relative(base+"/"+name+".bmp",std::filesystem::absolute(GAGCore::Toolkit::getFileManager()->getDir(0))).string();
  globalContainer->gfx->printScreen(file);gui.prepareLocalPresentation();gui.drawAll(0);globalContainer->gfx->nextFrame();
 };
 save(gui,base+"/staged-initial.game");
 std::ofstream metrics(base+"/simulation-metrics.csv");metrics<<"step,alive,hp,attacking\n";
 int chosen=-1;
 for(int step=0;step<=384;step++){
  if(step)gui.game.step(0);
  if(step%16==0){int n=0,hp=0,a=0;for(int t=0;t<2;t++)for(int j=0;j<Unit::MAX_COUNT;j++){auto*u=gui.game.teams[t]->myUnits[j];if(u&&u->typeNum==WARRIOR){n++;hp+=u->hp;a+=u->movement==Unit::MOV_ATTACKING_TARGET;}}
   metrics<<step<<","<<n<<","<<hp<<","<<a<<"\n";metrics.flush();
   if((step>=192&&a>=24&&n>=100&&chosen<0)||step==384){chosen=step;draw("terrain-candidate",0.4,174,100);save(gui,base+"/battle-state.game");std::cout<<"capture step="<<step<<" alive="<<n<<" hp="<<hp<<" attacking="<<a<<" center="<<cx<<","<<cy<<std::endl;break;}
  }
 }
 // Normal GameGUI adaptive overview, rather than a full-map exporter.
 
 }
 std::cout<<"done"<<std::endl;return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 1;}}
