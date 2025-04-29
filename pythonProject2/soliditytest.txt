package org.sde.cec.basicModel;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class soliditytest {
    public static void main(String[] args) {
        Process proc;
        try {
            // 指定虚拟环境中的 Python 解释器路径
            String pythonExecutable = "D:\\pythonProject1\\venv\\Scripts\\python.exe";  // Windows 示例
            String scriptPath = "D:\\pythonProject1\\main.py";  // Python 脚本路径

            // 运行 Python 脚本
            proc = Runtime.getRuntime().exec(pythonExecutable + " " + scriptPath);

            // 读取标准输出流
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println("Output: " + line);
            }
            in.close();

            // 读取标准错误流
            BufferedReader errorIn = new BufferedReader(new InputStreamReader(proc.getErrorStream()));
            while ((line = errorIn.readLine()) != null) {
                System.err.println("Error: " + line);
            }
            errorIn.close();

            // 等待 Python 进程执行完毕
            proc.waitFor();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
