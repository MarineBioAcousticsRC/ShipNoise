% stolen from getShipsAIS_CINMS_B_180820.m -> BJT
% to work with Shipplotter decoded AIS files
% 180912 smw
clear variables

% set AIS decoded file type
aisType = 1; % SBARC=1, Shipplotter=2, Marine Cadastre

% nominal site B location is CINMS_B_30_00
% ~7.6 km from edge of southbound side of the shipping lane
siteB = [ 34.2755, -120.0185 ];

rlat = siteB(1) * pi/180;
% Ref: American Practical Naviagator, Bowditch 1958, table 6 (explanation)
% page 1187
m = 111132.09 - 566.05 * cos(2*rlat) + 1.2 * cos(4*rlat) - 0.003 * cos(6*rlat);
p = 111415.10 * cos(rlat) - 94.55 * cos(3*rlat) - 0.12 * cos(5*rlat);


% for starters, let's filter for any ships inside some lat/lon box
boundd_m = 20e3; % in [m]
maxLat = [ siteB(1)-boundd_m/m, siteB(1)+boundd_m/m ];
maxLon = [ siteB(2)-boundd_m/p, siteB(2)+boundd_m/p ];

switch aisType
    case 1
        % aisFiles = {
        %     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180713.txt';
        %     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180714.txt';
        %     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180715.txt';
        %     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180716.txt';
        %     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180717.txt';
        %     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180718.txt';
        %     };
        
        idir = 'F:\ShippingCINMS_data\SBARC';
        aisFiles = ls(fullfile(idir,'AIS_SBARC_*.txt'));
        odir = 'F:\ShippingCINMS\matFiles';
        aisTypeStr = 'SBARC';
    case 2
        %         idir = 'P:\ShippingCINMS\AIS\testCOP\';
        idir = 'P:\ShippingCINMS\AIS\COP\';
        aisFiles = ls(fullfile(idir,'shipplotter*.log'));
        %         odir = 'P:\ShippingCINMS\matFilesTest';
        odir = 'P:\ShippingCINMS\matFilesCOP';
        aisTypeStr = 'ShipPlotter';
        
    case 3
        % marine cadastre csv format (not geodatabases from 2014 and
        % earlier)
        idir = 'F:\MarineCadastre\CINMSonly';
        aisFiles = ls(fullfile(idir,'AIS*10-11*.csv'));
        aisTypeStr = 'MARCAD';

        odir = 'F:\MarineCadastre\matFilesMarCad';
    otherwise
        disp('unknown decoded AIS type')
        aisTypeStr = 'Unk';

end

if ~isfolder(odir) % no folder? make it
    mkdir(odir)
end

NF = size(aisFiles,1);
for f = 1:NF
    %     aisFile = aisFiles{f};
    aisFile = fullfile(idir,aisFiles(f,:));
    %     if ~isempty(strfind(aisFile,'NMEA'))
    if contains(aisFile,'NMEA') || contains(aisFile,'nmea')...
            && aisType~=3
        %don't want to use coded AIS
        continue
    end
    
    %     odir = 'G:\ShippingCINMS\matFiles';
    %     ofn = sprintf('siteB_AIS_10km_%s.mat',...
    %         datestr(floor(shipTracks(1).dnums(1)),'yymmdd'));
    if aisType ~=3
        dstamp = regexp(aisFile,'[0-9]{6}','match');
    else
        dstampOrig = char(regexp(aisFile,'[0-9]{4}_[0-9]{2}','match'));
        dstamp = {datestr(datenum([str2num(dstampOrig(1:4)),str2num(dstampOrig(6:7)),01]),'yymmdd')};
    end
    ofn = sprintf('siteB_AIS_%s_%dm_%s.mat',aisTypeStr,boundd_m,dstamp{1});
    offn = fullfile(odir,ofn);
    
    %     if exist(offn,'file') == 2 % output exists, don't process input
    %         disp([offn,' Output file already exist'])
    %         continue;
    %     end
    
    finfo = dir(aisFile);
    % on BJT machine processes ~350 kbytes/sec
    est_rt = (finfo.bytes/350e3)/60;
    [ ~, fname, ext ] = fileparts(aisFile);
    fprintf('%s: %s%s ~%.2f minutes to process\n', ...
        datestr(now,'mm/dd/yy HH:MM:SS'),fname,ext, est_rt);
    %     tic
    try
        switch aisType
            case 1
                [ msg13_char, msg13_num, msg5_char, msg5_num ] = parseDecodedSBARC_180814(aisFile);
            case 2
                [ msg13_char, msg13_num, msg5_char, msg5_num ] = parseDecodedShipplotter_180912(aisFile);
            case 3
                [ msg13_char, msg13_num, msg5_char, msg5_num ] = parseDecodedMarCadastre(aisFile);
                
            otherwise
                disp('unknown decoded AIS type')
        end
    catch ME
        fprintf('\tParse fail: %s\n',ME.message);
        continue
    end
    %     toc
    
    % work on message IDs 1-3 first
    lats = msg13_num(:,6);
    lons = msg13_num(:,5);
    
    %     msg13_char0 = msg13_char;
    %     msg13_num0 = msg13_num;
    xIdx = find(lats >= maxLat(1) & lats <= maxLat(2));
    yIdx = find(lons >= maxLon(1) & lons <= maxLon(2));
    
    clear lats lons
    gIdx = intersect(xIdx, yIdx);
    msg13_char = msg13_char(gIdx,:);
    msg13_num = msg13_num(gIdx,:);
    
    if ~isempty(msg13_num)
        shipTracks = struct;
        % get unique ships via MMSI number
        uShips = unique(msg13_num(:,2));
        fprintf('\t%d ships found:\n',length(uShips));
        sInc = 1;
        for s = 1:length(uShips)
            s13idx = find(msg13_num(:,2)==uShips(s));
            s5idx = find(msg5_num(:,2)==uShips(s));
            switch aisType
                case 1
                    shipTracksTemp.name = unique(msg13_char(s13idx,1));
                case 2
                    shipTracksTemp.name = unique(msg5_char(s5idx,1));
                case 3
                    shipTracksTemp.name = unique(msg13_char(s13idx,1));
                    s5idx = s13idx;
            end
            if isempty(shipTracksTemp.name)
                shipTracksTemp.name{1} = 'unknown';
            end
            fprintf('\t%s\n',shipTracksTemp.name{1});
            
            % sort times
            [timeStamps,timeIdx] = sort(msg13_num(s13idx,1));
            % decide if there are multiple passages of the same vessel.
            % by looking for gaps of >=30mins
            tDiff = diff(timeStamps);
            transitGaps = [0,find(tDiff>=(1/(24*4)))',length(timeStamps)];
            uTransits = length(transitGaps)-1;
            fprintf('\t\t%0.0f Passage(s) Found\n',uTransits);
            if uTransits>5
                1;
            end
            tStart = 1;
            thisShip_char_m5 = msg5_char(s5idx(timeIdx),:);
            thisShip_num_m13 = msg13_num(s13idx(timeIdx),:);
            thisShip_num_m5 = msg5_num(s5idx(timeIdx),:);
            
            for iT = 1:uTransits
                
                transitIdx = transitGaps(tStart)+1:transitGaps(tStart+1);
                [~,uTimes] = unique(thisShip_num_m13(transitIdx,1));
                shipTracks(sInc).dnums = thisShip_num_m13(transitIdx(uTimes),1);

                shipTracks(sInc).name = shipTracksTemp.name;
                shipTracks(sInc).shipType = unique(thisShip_char_m5(transitIdx(uTimes),2));
                shipTracks(sInc).MMSI = uShips(s);
                shipTracks(sInc).IMO = unique(thisShip_num_m5(transitIdx(uTimes),3));
                shipTracks(sInc).lons = thisShip_num_m13(transitIdx(uTimes),5);
                shipTracks(sInc).lats = thisShip_num_m13(transitIdx(uTimes),6);
                shipTracks(sInc).SOG = thisShip_num_m13(transitIdx(uTimes),4);
                shipTracks(sInc).COG = thisShip_num_m13(transitIdx(uTimes),7);
                shipTracks(sInc).trueHeading = thisShip_num_m13(transitIdx(uTimes),8);
                % voyage data - datenum, IMO, draught, dimensions ( toBow, toStern, toPort,
                % toStarboard )
                if aisType ~=3
                    shipTracks(sInc).vData = [ thisShip_num_m5(transitIdx(uTimes),1), thisShip_num_m5(transitIdx(uTimes),3:8) ];
                else
                    shipTracks(sInc).vData = [thisShip_num_m13(transitIdx(uTimes),1),thisShip_num_m5(transitIdx(uTimes),1),...
                        thisShip_num_m5(transitIdx(uTimes),4:9) ];
                end
%                
%                 figure(101);
%                 plot(shipTracks(sInc).lats,shipTracks(sInc).lons,'o')
%                 hold on
%                 plot(siteB(1),siteB(2),'ok')
%                 hold off 
                                
                
                tStart = tStart+1;
                sInc = sInc+1;
            end
        end
        save(offn,'shipTracks');
    else
        fprintf('No ships within bounds found\n');
    end
end

