%% Machine Learning - Project - Analyse results
clc;

format long

filename = 'random_4_160421_r5.csv';
M = csvread(filename,1,0);
runs = length(M)

%% General analysis

minMoves = min(M(:,1))
maxMoves = max(M(:,1))
avgMoves = mean(M(:,1))
stdMoves = std(M(:,1))

minScore = min(M(:,3))
maxScore = max(M(:,3))
avgScore = mean(M(:,3))
stdScore = std(M(:,3))

minTile = min(M(:,2))
maxTile = max(M(:,2))
avgTile = mean(M(:,2))
stdTile = std(M(:,2))

figure(1)
histogram(M(:,3),100)
xlim([minScore maxScore])

%% Per max tile analysis

F8 = M((M(:, 2) == 8),:);
F16 = M((M(:, 2) == 16),:);
F32 = M((M(:, 2) == 32),:);
F64 = M((M(:, 2) == 64),:);
F128 = M((M(:, 2) == 128),:);
F256 = M((M(:, 2) == 256),:);
F512 = M((M(:, 2) == 512),:);

% number of runs that finished with specific max tile
v = [8; 16; 32; 64; 128; 256; 512];
p = [length(F8); length(F16); length(F32); length(F64); length(F128); length(F256); length(F512)];
r = [v p]

figure(2)
clf
xlim([minScore maxScore])
bins = 10;
hold on
histogram(F32(:,3),bins)
histogram(F64(:,3),bins)
histogram(F128(:,3),bins)
histogram(F256(:,3),bins)
hold off
legend('max tile: 32','max tile: 64','max tile: 128','max tile: 256')



