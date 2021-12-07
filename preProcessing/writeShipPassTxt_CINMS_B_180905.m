function writeShipPassTxt_CINMS_B_180905(ofroot, odir, siteB, dataID, PA, shipTracks, t0, tn,d)

% TODO 
%   add in filtering for unavailable info 
%   add in conversion of ship type to something meaningful
%
mnum2secs = 24*60*60;
secs2mnum = 1/mnum2secs;
date_fmt = 'mm/dd/yyyy HH:MM:SS';

fprintf('%s\t%s - %s (%.2f seconds)\n', ...
    shipTracks.name{1}, ...
    datestr(t0,date_fmt),datestr(tn,date_fmt),...
    (tn-t0)*mnum2secs);

[ dx, dy ] = arrayfun(@(x,y) latlon2xy(x,y,siteB(1),siteB(2)), ...
    shipTracks.lats,shipTracks.lons);
d = arrayfun(@(x,y) sqrt(x^2+y^2), dx, dy);
[ cpa_m, cpai ] = min(d);
        
fprintf('%s\n', ofroot);
fprintf('HARP site %s\n', dataID);
fprintf('CPA = %.2f km @ \n\n', cpa_m/1e3);

ofn1 = sprintf('%s.txt', ofroot);
offn1 = fullfile(odir,ofn1);

% open text file and write info on ship pass
fod = fopen(offn1,'w');
fprintf(fod,'HARPSite=%s\n',dataID);
fprintf(fod,'HARPLat=%.5f\n',siteB(1));
fprintf(fod,'HARPLon=%.5f\n',siteB(2));
fprintf(fod,'PreAmp=%s\n', PA);
fprintf(fod,'CPATime[UTC]=%s\n',datestr(shipTracks.dnums(cpai),date_fmt));
fprintf(fod,'CPADistance[m]=%.2f\n', cpa_m);
fprintf(fod,'ShipName=%s\n', shipTracks.name{1});
fprintf(fod,'MMSI=%d\n',shipTracks.MMSI);
if ~isempty(shipTracks.IMO)
    fprintf(fod,'IMO=%d\n',shipTracks.IMO);
end
if ~isempty(shipTracks.shipType)
    stype = unique(shipTracks.shipType);
    fprintf(fod,'ShipType=%s\n',stype{1}); 
end
% assume draught, dimensions don't change
if ~isempty(shipTracks.vData)
    draught = shipTracks.vData(1,3);
    toBow = shipTracks.vData(1,4);
    toStern = shipTracks.vData(1,5);
    toPort = shipTracks.vData(1,6);
    toStarboard = shipTracks.vData(1,7);
    fprintf(fod,'Draught[m]=%.2f\n',draught); 
    fprintf(fod,'toBow[m]=%.1f\n',toBow); 
    fprintf(fod,'toStern[m]=%.1f\n',toStern);
    fprintf(fod,'toPort[m]=%.1f\n',toPort);
    fprintf(fod,'toStarboard[m]=%.1f\n',toStarboard);
end

% write out trackline info
trackHdr = 'UTC,latitude,longitude,trueHeading,SOG,COG,range\n';
fprintf(fod,trackHdr);
shipTracks.dStr = datestr(shipTracks.dnums,date_fmt);
arrayfun(@(x) fprintf(fod,'%s,%.5f,%.5f,%d,%.1f,%.1f,%.1f\n',...
    shipTracks.dStr(x,:),...
    shipTracks.lats(x),...
    shipTracks.lons(x),...
    shipTracks.trueHeading(x),...
    shipTracks.SOG(x),...
    shipTracks.COG(x),...
    d(x)), 1:length(shipTracks.lats),'UniformOutput',0);
fclose(fod);
1;



