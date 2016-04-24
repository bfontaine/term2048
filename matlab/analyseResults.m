%% Machine Learning - Project - Analyse results
clc;

format shortG

filename = '/Users/Ajrok/Dropbox/MachineLearning/results/random_4_160421_r6.csv';
M = csvread(filename,1,0);
runs = length(M)

%% General analysis

Moves = [min(M(:,1)); median(M(:,1)); max(M(:,1)); mean(M(:,1)); std(M(:,1))];
Score = [min(M(:,3)); median(M(:,3)); max(M(:,3)); mean(M(:,3)); std(M(:,3))];
maxTile = [min(M(:,2)); median(M(:,2)); max(M(:,2)); mean(M(:,2)); std(M(:,2))];

rows = {'Min';'Med';'Max';'Avg';'Std'};
T = table(Moves,Score,maxTile,'RowNames',rows)

figure(1)
histogram(M(:,3),100)
xlim([Score(1) Score(3)])

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
n = [length(F8); length(F16); length(F32); length(F64); length(F128); length(F256); length(F512)];
p = n./runs;

columns = {'maxTile';'numberOfRuns';'part'};
R = table(v,n,p,'VariableNames',columns)

figure(2)
clf
xlim([Score(1) Score(3)])
bins = 10;
hold on
histogram(F32(:,3),bins)
histogram(F64(:,3),bins)
histogram(F128(:,3),bins)
histogram(F256(:,3),bins)
hold off
legend('max tile: 32','max tile: 64','max tile: 128','max tile: 256')



