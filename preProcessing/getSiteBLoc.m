function [ siteB, dataID,PA ] = getSiteBLoc(dnum)


% nominal site B location is CINMS_B_30_00	
% ~7.6 km from edge of southbound side of the shipping lane
% ~3.5 km from edge of northbound lane
% need to add in code that looks up site location based on time period!
siteB = [ 34.2755, -120.0185 ];
dataID = [];
PA = '';

%load('D:\Projects\ShippingCINMS\code\matlab\CINMS_B_depInfo.mat');
load('E:\Data\ShippingCINMS\CINMS_B_depInfo');
si = find(recTimes(:,1) <= dnum,1,'last');
ei = find(recTimes(:,2) >= dnum,1,'first');

if isempty(si) && isempty (ei)
    fprintf('No HARP deployment found for this time period...skipping\n');
    return;
elseif isempty(si) || isempty(ei)
    fprintf('Partial HARP deployment found for this time period...skipping\n'); 
    return;
elseif si<ei 
    fprintf('Multiple HARP deployment found for this time period...skipping!!!!\n');
    return;
end

siteB = [ lats(si), lons(si) ];
dataID = names{si};
PA = preAmp{si};