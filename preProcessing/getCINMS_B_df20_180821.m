function [ data ] = getCINMS_B_df20_180821(t0,tn)


% load xwav time mat files ( made with getXWAVTimes_CINMS_B.m )
% these include a full pathname so may need to be regenerated if mount
% points change ( i.e. disk has been disconnected/reconnected )
%
xwavTimes = {
    'E:\Data\ShippingCINMS\CINMS_B_xwavInfo_000113_to_151216.mat';
    'E:\Data\ShippingCINMS\CINMS_B_xwavInfo_151216_to_180205.mat'};

mnum2secs = 24*60*60;
date_fmt = 'mm/dd/yy HH:MM:SS.FFF';
xffn = '';
xt = [];

% might need to save xwav start/end times instead of LTSA start/end times 
% this script will be called 1000+ times
for f = 1:length(xwavTimes)
    clear ltsaInfo 
    load(xwavTimes{f});
    xffn = [ xffn; xwavs ];
    xt = [ xt; xtimes ];
    1;
end

[ ~, sorti ] = sort(xt(:,1));
xt = xt(sorti,:); 
xffn = xffn(sorti,:);

si = find(xt(:,1) <= t0,1,'last');
ei = find(xt(:,2) >= tn,1,'first');

if si > ei
%     fprintf('SOMETHING IS WRONG\n');
    fprintf('Time period is found in two non-sequential raw files...skipping \n');
    data = [];
    return;
elseif isempty(ei) || isempty(si) 
    fprintf('No available xwav data for this period\n');
    data = [];
    return;
end

% if (tn-t0)*mnum2secs > 3600
%     1;
% end

data = [];
for x = si:ei
    t0str = datestr(t0,date_fmt);
    tnstr = datestr(tn,date_fmt);
    datat = get_xwav_data_1ch( strrep(xffn(x,:),char(0),'') , t0str, tnstr );
    data = [ data; datat ];
end

% add in code to log when we can't find data ( i.e. not in our set of xwavs
% )