/* Clang front end header files */
#include "clang/Driver/Options.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/ASTConsumers.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "clang/Rewrite/Core/Rewriter.h"

/* Other headers */
#include <iostream>
#include "vector"
#include <tuple>
#include "ASTVisitor.h"
#include "ASTTraverser.h"
#include <fstream>

using namespace std;
using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace llvm;

typedef vector< tuple<string,string, string, string, string, string, string> > myList;

Rewriter rewriter;
CompilerInstance* mainCI;
int numFunctions = 0;

myList* varList = new myList();


/* Apply a custom category to all command-line options so that they are the only ones displayed. */
llvm::cl::OptionCategory MyToolCategory("my-tool options");

string getRawCodeAsString(SourceRange sr) {
    return rewriter.getRewrittenText(sr);
}

class NodeTraverser : public ASTTraverser {
    friend ASTTraverser;

    void ActionBinaryOperator(clang::BinaryOperator* bop) {
        if(bop->isAssignmentOp() && bop->getType()->isFloatingType()) {
            outs() << "Assignment detected\n";
            //bop->dump(); /* Print AST of this node */
            outs() << getRawCodeAsString(bop->getSourceRange()) << "\n";
        }
    }

public:
    template<typename T>
    explicit NodeTraverser(T* st) {
        _traverseAST(st);
    }
};

class ASTMainVisitor : public RecursiveASTVisitor<ASTMainVisitor> {
    friend RecursiveASTVisitor<ASTMainVisitor>;

    /* Context used for getting additional AST info */
    ASTContext* astMainContext;
    SourceLocation processedLocation;

    bool ActionFunctionDecl(FunctionDecl *fund) {
        numFunctions++;
        string funcName = fund->getNameAsString();
        //outs() << funcName << " found\n";

        if (fund->doesThisDeclarationHaveABody()) {
//            /* Traverse AST below this node */
//            Stmt* body = fund->getBody();
//            NodeTraverser n(body);
        }

        return true;
    }


    bool ActionVarDecl(VarDecl *var) {
        //SourceRange varLocRange = var->getSourceRange();

        //if(!var->getType()->isRealFloatingType()) {
            /* Return if it is not floating point. This does not support pointers, e.g. double*. */
        //    return true;
        //}

//        outs() << var->getType().getAsString() << "\n";

        /* To handle same-line-declarations, test that begin location is not already processed */
        //if (processedLocation < varLocRange.getBegin()) {
        //    SourceRange typeRange = var->getTypeSourceInfo()->getTypeLoc().getSourceRange();

        //    rewriter.ReplaceText(typeRange, "real_t");
        //}
        string typeBeg = "";
        string typeEnd = "";
        string varName = "";
        string initBeg = "";
        string initEnd = "";

        typeBeg = var->getTypeSourceInfo()->getTypeLoc().getSourceRange().getBegin().printToString(rewriter.getSourceMgr());
        typeEnd = var->getTypeSourceInfo()->getTypeLoc().getSourceRange().getEnd().printToString(rewriter.getSourceMgr());
        varName = var->getDeclName().getAsString();

        if(var->hasInit()){
          initBeg = var->getInit()->getSourceRange().getBegin().printToString(rewriter.getSourceMgr());
          initEnd = var->getInit()->getSourceRange().getEnd().printToString(rewriter.getSourceMgr());
        }

        string begin = var->getSourceRange().getBegin().printToString(rewriter.getSourceMgr());
        string end = var->getSourceRange().getEnd().printToString(rewriter.getSourceMgr());

        auto tup = make_tuple(typeBeg, typeEnd, varName, initBeg, initEnd, begin, end);
        varList->push_back(tup);
        //has definition? has init?
        //processedLocation = varLocRange.getEnd();
        return true;
    }

    /* There are two main parent classes in the clang AST, namely Stmt and Decl. Most of the nodes
     * are derived from them. An exception is AttributedStmt. This node is not caught by VisitStmt. */
    bool VisitStmt(Stmt *st) {

        /* Check that the statement is in the main file. If not, it is most likely in a header file*/
        SourceManager& SM = rewriter.getSourceMgr();
        if (!SM.isInMainFile(st->getBeginLoc())) {
            /* The current location is not in the main file. Do not process.
             * (It is most likely in a header file.) */
            return true;
        }

        /* Process expression, e.g. binary expression, function calls, etc */
        if (auto *expr  = dyn_cast<Expr>(st)) {
            return true;
        }

        /* Process if-else statement */
        if (auto *ifs = dyn_cast<IfStmt>(st)) {
            return true;
        }

        /* Process while-loop conditions */
        if (auto *whs = dyn_cast<WhileStmt>(st)) {
            return true;
        }

        /* Process for-loop */
        if (auto *frs = dyn_cast<ForStmt>(st)) {
            return true;
        }

        /* Process do-while */
        if (auto *dws = dyn_cast<DoStmt>(st)) {
            return true;
        }

        /* Process return statement */
        if (auto *res = dyn_cast<ReturnStmt>(st)) {
            res->getBeginLoc();
            cout << "hi\n";
            return true;
        }
        return true;
    }

    bool VisitDecl(Decl* decl) {
        SourceManager& SM = rewriter.getSourceMgr();
        if (!SM.isInMainFile(decl->getLocation())) {
            /* The current location is not in the main file. Do not process.
             * (It is most likely in a header file.) */
            return true;
        }

        if (auto *fund = dyn_cast<FunctionDecl>(decl)) {
            return ActionFunctionDecl(fund);
        }

        if (auto *fld = dyn_cast<FieldDecl>(decl)) {
            return true;
        }

        if (auto *var = dyn_cast<VarDecl>(decl)) {
            return ActionVarDecl(var);
        }

        if (auto *tyd = dyn_cast<TypedefDecl>(decl)) {
            return true;
        }

        return true;
    }

public:
    explicit ASTMainVisitor(CompilerInstance *CI) : astMainContext(&(CI->getASTContext())) {
        mainCI = CI;
        rewriter.setSourceMgr(astMainContext->getSourceManager(), astMainContext->getLangOpts());
    }
};

class ExampleASTConsumer : public ASTConsumer {
private:
    ASTMainVisitor *visitor; // doesn't have to be private

public:
    /* Override the constructor in order to pass CI */
    explicit ExampleASTConsumer(CompilerInstance *CI)
            : visitor(new ASTMainVisitor(CI)) // initialize the visitor
    { }

    /* Override this to call our ASTMainVisitor on the entire source file */
    void HandleTranslationUnit(ASTContext &Context) override {
        /* ASTContext is used to get the TranslationUnitDecl (a declaration representing the entire source file). */
        TranslationUnitDecl* tud = Context.getTranslationUnitDecl();

        /* Now traverse the entire main visitor to perform the interval transformations */
        visitor->TraverseDecl(tud);
    }
};

class ExampleFrontendAction : public ASTFrontendAction {
public:
    ExampleFrontendAction() = default;

    void EndSourceFileAction() override {
        /* Do something when end of source is reached */
    }

    virtual std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI, StringRef file) override {
        return (std::unique_ptr<ASTConsumer>) new ExampleASTConsumer(&CI); // pass CI pointer to ASTConsumer
    }
};

int main(int argc, const char **argv) {
    if(argc != 5){
      cout << "Error: wrong number of arguments:\n";
      return -1;
    }

    string file_path = argv[3];
    string file_name = argv[4];

    CommonOptionsParser op(argc, argv, MyToolCategory);

    /* create a new Clang Tool instance (a LibTooling environment) */
    ClangTool Tool(op.getCompilations(), op.getSourcePathList());

    /* run the Clang Tool, creating a new FrontendAction */
    int result = Tool.run(newFrontendActionFactory<ExampleFrontendAction>().get());


    /* print out the rewritten source code */
    //errs() << "\nFound " << numFunctions << " functions.\n\n";
    //FileID fid = rewriter.getSourceMgr().getMainFileID();
    //rewriter.getEditBuffer(fid).write(outs());
    ofstream myfile;
    myfile.open (file_path + "vars.txt");
    for(size_t i = 0; i < varList->size(); i++){
        myfile << get<0>(varList->at(i)) << "\n";
        myfile << get<1>(varList->at(i)) << "\n";
        myfile << get<2>(varList->at(i)) << "\n";
        myfile << get<3>(varList->at(i)) << "\n";
        myfile << get<4>(varList->at(i)) << "\n";
        myfile << get<5>(varList->at(i)) << "\n";
        myfile << get<6>(varList->at(i)) << "\n";
    }
    myfile.close();

    return result;
}
