clear variables
% nominal site B location is CINMS_B_30_00	
% ~7.6 km from edge of southbound side of the shipping lane
siteB = [ 34.2755, -120.0185 ];

rlat = siteB(1) * pi/180;
% Ref: American Practical Naviagator, Bowditch 1958, table 6 (explanation)
% page 1187
m = 111132.09 - 566.05 * cos(2*rlat) + 1.2 * cos(4*rlat) - 0.003 * cos(6*rlat);
p = 111415.10 * cos(rlat) - 94.55 * cos(3*rlat) - 0.12 * cos(5*rlat);


% for starters, let's filter for any ships inside some lat/lon box
boundd_m = 15e3; % in [m]
maxLat = [ siteB(1)-boundd_m/m, siteB(1)+boundd_m/m ]; 
maxLon = [ siteB(2)-boundd_m/p, siteB(2)+boundd_m/p ];

% aisFiles = {
%     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180713.txt';
%     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180714.txt';
%     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180715.txt';
%     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180716.txt';
%     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180717.txt';
%     'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180718.txt';
%     };

idir = 'D:\Projects\ShippingCINMS\AIS\SBARC\';
aisFiles = ls(fullfile(idir,'AIS_SBARC_*.txt'));



for f = 1:length(aisFiles)
%     aisFile = aisFiles{f};
    aisFile = fullfile(idir,aisFiles(f,:));
    if ~isempty(strfind(aisFile,'NMEA'))
        %don't want to use coded AIS
        continue
    end
    
    odir = 'D:\Projects\ShippingCINMS\matFiles';
%     ofn = sprintf('siteB_AIS_10km_%s.mat',...
%         datestr(floor(shipTracks(1).dnums(1)),'yymmdd'));
    dstamp = regexp(aisFile,'[0-9]{6}','match');
    ofn = sprintf('siteB_AIS_%dm_%s.mat',boundd_m,dstamp{1});    
    offn = fullfile(odir,ofn);
    
    if exist(offn,'file') == 2 % output exists, don't process input
        continue;
    end
    
    finfo = dir(aisFile);
    % on BJT machine processes ~350 kbytes/sec
    est_rt = (finfo.bytes/350e3)/60;
    [ ~, fname, ext ] = fileparts(aisFile);
    fprintf('%s: %s%s ~%.2f minutes to process\n', ...
        datestr(now,'mm/dd/yy HH:MM:SS'),fname,ext, est_rt);
%     tic
    try
        [ msg13_char, msg13_num, msg5_char, msg5_num ] = parseDecodedSBARC_180814(aisFile);
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
        for s = 1:length(uShips)
            s13idx = find(msg13_num(:,2)==uShips(s));
            s5idx = find(msg5_num(:,2)==uShips(s));
            shipTracks(s).name = unique(msg13_char(s13idx,1));
            fprintf('\t%s\n',shipTracks(s).name{1});
            shipTracks(s).shipType = msg5_char(s5idx,2);
            shipTracks(s).MMSI = uShips(s);
            shipTracks(s).IMO = unique(msg5_num(s5idx,3));
            shipTracks(s).lons = msg13_num(s13idx,5);
            shipTracks(s).lats = msg13_num(s13idx,6);
            shipTracks(s).dnums = msg13_num(s13idx,1);
            shipTracks(s).SOG = msg13_num(s13idx,4);
            shipTracks(s).COG = msg13_num(s13idx,7);
            shipTracks(s).trueHeading = msg13_num(s13idx,8);
            % voyage data - datenum, IMO, draught, dimensions ( toBow, toStern, toPort,
            % toStarboard )
            shipTracks(s).vData = [ msg5_num(s5idx,1), msg5_num(s5idx,3:8) ]; 
        end

        save(offn,'shipTracks');
    else
        fprintf('No ships within bounds found\n');
    end
end

