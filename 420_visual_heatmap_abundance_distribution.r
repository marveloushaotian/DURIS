library(ComplexHeatmap)
library(circlize)
library(grid)

# 设置固定参数
input_dir <- "Collect/01_Defense/03_Defense_TPM_Abundance_Matrix/Inuse/"  # 请替换为您的输入目录路径
output_dir <- "Results/03_DF_abun_distribution/Heatmap/Distribution2/"  # 请替换为您的输出目录路径
min_nonzero <- 0
figure_width <- 10  # 以英寸为单位
figure_height <- 8  # 以英寸为单位
fontsize <- 10

# 创建自定义颜色映射
create_custom_colormap <- function() {
  colors <- c('#eaeeea', '#d6ecc1', '#b9df89', '#99ce76',
              '#75b989', '#54a296', '#458689', '#3a6a77')
  return(colorRamp2(seq(0, 1, length = length(colors)), colors))
}

# 生成热图函数
generate_heatmap <- function(file_path, save_path, min_nonzero, figure_width, figure_height, fontsize, custom_cmap) {
  data <- read.csv(file_path, row.names = 1)
  filtered_data <- data[rowSums(data != 0) >= min_nonzero, ]
  
  # 对数据进行对数转换
  log_data <- log10(filtered_data + 1)
  
  # 创建热图
  ht <- Heatmap(as.matrix(log_data),
                name = "Log10(Abundance + 1)",
                col = custom_cmap,
                show_row_names = TRUE,
                show_column_names = TRUE,
                cluster_rows = TRUE,
                cluster_columns = TRUE,
                row_names_gp = gpar(fontsize = fontsize),
                column_names_gp = gpar(fontsize = fontsize),
                heatmap_legend_param = list(
                  title_gp = gpar(fontsize = fontsize),
                  labels_gp = gpar(fontsize = fontsize)
                ))
  
  # 保存热图
  filename <- sub("\\.csv$", "_heatmap.pdf", basename(file_path))
  pdf(file.path(save_path, filename), width = figure_width, height = figure_height)
  draw(ht)
  dev.off()
}

# 主函数
main <- function() {
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  custom_cmap <- create_custom_colormap()
  
  csv_files <- list.files(input_dir, pattern = "\\.csv$", full.names = TRUE)
  
  for (file_path in csv_files) {
    generate_heatmap(file_path, output_dir, min_nonzero, figure_width, figure_height, fontsize, custom_cmap)
  }
  
  print("热图已生成并成功保存。")
}

# 运行主函数
main()