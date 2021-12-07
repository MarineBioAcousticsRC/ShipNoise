function plotShipPass_CINMS_B_180821(h,dx,dy,shipTracks,s,cpa_m,t0,tn,irad_m)


date_fmt = 'mm/dd/yy HH:MM:SS';
mnum2secs = 24*60*60;
secs2mnum = 1/mnum2secs;
        
% get TF
tfIdx = find(~cellfun(@isempty,strfind(tfList.textdata(:,1),siteName)));
tfNum = tfList.data(tfIdx-1);
[tfFolder, TFName] = pick_TF_subdirs(tfNum,tfDir);

%tfFolder = dir(fullfile(tfDir,[num2str(tfNum),'*']));
tfFile = fullfile(tfFolder,TFName.name); % dir(fullfile(tfFolder.folder,tfFolder.name,'*.tf'));

if isempty(tfFile)
    error('missing tf file')
end


% build title string for plot
titleStr = sprintf('%s',shipTracks(s).name{1});
if ~isempty(shipTracks(s).IMO)
    titleStr = sprintf('%s IMO = %d',titleStr,shipTracks(s).IMO);
end

titleStr = sprintf('%s\nMMSI = %d',titleStr,shipTracks(s).MMSI);
titleStr = sprintf('%s\nMean SOG = %.2f [ kn ] CPA = %.2f [ m ]', ...
    titleStr, mean(shipTracks(s).SOG), cpa_m);
if ~isempty(shipTracks(s).vData)
    titleStr = sprintf('%s draught = %.2f [m]', titleStr,mean(shipTracks(s).vData(:,3)));
end
titleStr = sprintf('%s\n%s - %s UTC',titleStr,datestr(t0,date_fmt),datestr(tn,date_fmt));

FS = 10;
set(h,'Position',[ 75 75 720 720 ] );
np = length(dx);
cmap = jet(np);

plot(0,0,'LineWidth',5,'Marker','o','MarkerEdgeColor','k','MarkerFaceColor','k');
hold on
for p=1:length(dx)
    plot(dx(p),dy(p),'Marker','o','Color',cmap(p,:));
end
axis([ -irad_m irad_m -irad_m irad_m ]);
ax = gca;
ap = get(ax,'Position');
set(ax,'Position',[ap(1) ap(2) ap(3)*.9 ap(4)*.9]);


hold off
grid minor
%         cb = colorbar('Location','SouthOutside','Position',[0.12 0.075 0.8 0.0125],'FontSize',FS);
cb = colorbar('Location','EastOutside','Position',[ .85 .1 0.0125 0.75],'FontSize',FS);
colormap(jet)
set(gca,'TickDir','out');
cbtickint_s = 150;
cbticks = [0:cbtickint_s*secs2mnum:tn-t0]./(tn-t0);
cbticklabels = datestr(t0:cbtickint_s*secs2mnum:tn,'HH:MM:SS');  % will this and the ticks always match up nicely?
set(cb,'Ticks', cbticks);
set(cb,'TickLabels', cbticklabels);
xlabel(ax,'W-E [m]');
ylabel(ax,'S-N [m]');
t = title(titleStr);
tp = get(t,'Position');
set(t,'Position', [ tp(1) tp(2)+100 tp(3) ]);