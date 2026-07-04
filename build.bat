@echo off
chcp 65001 >nul
echo ========================================
echo   TestCraft 打包脚本
echo   智能测试用例生成器 v1.0
echo ========================================
echo.

echo [1/3] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist TestCraft.spec del /q TestCraft.spec
echo 清理完成。
echo.

echo [2/3] 使用 PyInstaller 打包...
pyinstaller ^
    --name "TestCraft" ^
    --windowed ^
    --icon "assets/testcraft.ico" ^
    --add-data "testcase_generator;testcase_generator" ^
    --hidden-import "testcase_generator.models" ^
    --hidden-import "testcase_generator.engine" ^
    --hidden-import "testcase_generator.codegen" ^
    --hidden-import "testcase_generator.exporter" ^
    --hidden-import "testcase_generator.theme" ^
    --hidden-import "testcase_generator.ui_sidebar" ^
    --hidden-import "testcase_generator.ui_dialogs" ^
    --hidden-import "testcase_generator.ui_dashboard" ^
    --hidden-import "testcase_generator.ui_project" ^
    --hidden-import "testcase_generator.ui_scenario_manager" ^
    --hidden-import "testcase_generator.ui_case_manager" ^
    --hidden-import "testcase_generator.ui_export" ^
    --hidden-import "testcase_generator.ui_statistics" ^
    --hidden-import "testcase_generator.ui_mainwindow" ^
    --noconfirm ^
    --clean ^
    main.py
echo.

if exist dist\TestCraft.exe (
    echo [3/3] 打包完成！
    echo.
    echo 📦 可执行文件位置: dist\TestCraft.exe
    echo.
    echo ========================================
    echo   打包成功！
    echo ========================================
) else (
    echo ❌ 打包失败！请检查上面的错误信息。
)

echo.
pause
